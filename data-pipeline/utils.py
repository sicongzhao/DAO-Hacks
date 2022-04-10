import requests
import json
import pandas as pd
import numpy as np
import math

snapshot_api = 'https://hub.snapshot.org/graphql'
covalent_api = 'https://api.covalenthq.com/v1/'
covalent_key = 'ckey_1c9890fa556c457ab9ff050c2f4'

ens_token_addr = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72' # for testing purpose

latest_block = 14555320
max_r_blocks = 1000000

daoinfo = pd.read_csv('../data/daoinfo.csv')
votes = pd.read_csv('../data/snapshot_votes.csv')
proposals = pd.read_csv('../data/snapshot_proposals.csv')
members = pd.read_csv('../data/members_summary.csv')




GET_PROPOSALS = """
query ($first:Int!, $skip:Int!, $space_in:[String]!) {
  proposals (
    first: $first,
    skip: $skip,
    where: {
      space_in: $space_in,
    },
    orderBy: "created",
    orderDirection: desc
  ) {
    id
    type
    title
    body
    choices
    start
    end
    snapshot
    state
    author
    space {
      id
      name
    }
  }
}
"""

GET_VOTES = """query ($first:Int!, $skip:Int!, $proposal:String!) {
  votes (
    first: $first
    skip: $skip
    where: {
      proposal: $proposal
    }
    orderBy: "created",
    orderDirection: desc
  ) {
    id
    voter
    created
    proposal {
      id
    }
    choice
    space {
      id
    }
  }
}
"""

# Helper functions
def request_proposals(governance):
    r = requests.post(snapshot_api, json={
        'query': GET_PROPOSALS, 
        'variables': {
            'first': 10000,
            'skip': 0,
            'space_in': [governance]
        }
    })
    print('Status:', r.status_code)
    return json.loads(r.text)['data']['proposals']

def request_votes(proposal_id):
    r = requests.post(snapshot_api, json={
        'query': GET_VOTES, 
        'variables': {
            'first': 100000,
            'skip': 0,
            'proposal': proposal_id
        }
    })
    print('Status:', r.status_code)
    return json.loads(r.text)['data']['votes']

def request_covalent(url):
    r = requests.get(url)
    if r.status_code == 200:
        print('request succeeded!')
        return json.loads(r.text)
    else:
        print('Request Error:', r)
        
def r_token_holder_url(network_id, token_address, page_size, page_number, block_height):
    r_url = covalent_api + str(network_id) + '/tokens/' + str(token_address) + '/token_holders/?quote-currency=USD&format=JSON&page-size=' + str(page_size) + '&page-number=' + str(page_number) + '&block-height=' + str(block_height) + '&key=' + covalent_key
    return request_covalent(r_url)


def r_log_events_url(network_id, address, page_size=10000, start_block=latest_block-max_r_blocks, end_block=latest_block):
    r_url = covalent_api + str(network_id) + '/events/address/' + str(address) + '/?starting-block=' + str(start_block) + '&ending-block=' + str(end_block) + '&page-size=' + str(page_size) + '&key=' + covalent_key
    print(r_url)
    return request_covalent(r_url)

def r_token_balance(network_id, address):
    r_url = covalent_api + str(network_id) + '/address/' + str(address) + '/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=' + covalent_key
    return request_covalent(r_url)

def r_portfolio_hist_val(network_id, address):
    r_url = covalent_api + str(network_id) + '/address/' + str(address) + '/portfolio_v2/?&key=' + covalent_key
    return request_covalent(r_url)

# Statistics
def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # All values are treated equally, arrays must be 1d:
    array = np.array(array)
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def remove_outliers_by_std(data, m=10.):
    """Remove outliers"""
    data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return data[s < m]

def isNaN(num):
    return num != num

def remove_outliers_by_rank(data, u=10, l=10):
    if len(data < u + l):
        return data
    else:
        data = np.array(data)
        for i in range(u):
            data = np.delete(data, data.argmax())
        for i in range(l):
            data = np.delete(data, data.argmin())
        return data

def calc_poll_detail_stats(proposal_res, token_address, block_height):
    num_of_choices = proposal_res.shape[0]
    voter_lists = proposal_res['voter_list'].values
    
    r = r_token_holder_url(1, token_address, 100000, 0, block_height)
    poll_historical_balance = {}
    for i in r['data']['items']:
        poll_historical_balance[i['address']] = int(i['balance'])

    poll_stats = []
    prev_max_balance = 0
    win_choice_id = -1
    total_token = 0
    for j in range(len(voter_lists)):
        temp = {
            'voters': len(voter_lists[j]),
            'tokens': 0
        }
        for a in voter_lists[j]:
            if a.lower() in poll_historical_balance.keys():
                temp['tokens'] += poll_historical_balance[a.lower()]
                total_token += poll_historical_balance[a.lower()]
                if temp['tokens'] > prev_max_balance:
                    win_choice_id = j
                    prev_max_balance = temp['tokens']
        poll_stats.append(temp)
    
    winner = poll_stats[win_choice_id]
    
    
    if total_token > 0 and winner['voters'] > 0 and total_votes > 0:
        token_rate = winner['tokens']/total_token
        voter_rate = winner['voters']/total_votes
        agreement_coefficient = token_rate/voter_rate
    else:
        agreement_coefficient = math.nan
        token_rate = math.nan
        voter_rate = math.nan
    return token_rate, voter_rate, agreement_coefficient