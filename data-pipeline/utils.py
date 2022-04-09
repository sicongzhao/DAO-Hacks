import requests
import json
import pandas as pd
import numpy as np
import math

snapshot_api = 'https://hub.snapshot.org/graphql'
covalent_api = 'https://api.covalenthq.com/v1/'
covalent_key = 'ckey_1c9890fa556c457ab9ff050c2f4'

ens_token_addr = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72' # for testing purpose

latest_block = 14548652
max_r_blocks = 1000000

df = pd.read_csv('../data/dao-data.csv')
votes = pd.read_csv('../data/snapshot_votes.csv')
proposals = pd.read_csv('../data/snapshot_proposals.csv')
members = pd.read_csv('../data/members.csv')




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

def reject_outliers(data, m=100.):
    """Remove outliers"""
    data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return data[s < m]

def isNaN(num):
    return num != num