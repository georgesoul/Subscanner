import requests
import argparse


def passivetotal_get(path, query):
    username = '<username>'
    key = '<your-token>'
    auth = (username, key)
    base_url = 'https://api.passivetotal.org'
    url = base_url + path
    data = {'query': query}
    response = requests.get(url, auth=auth, json=data)
    response = response.json()
    response = response.get('subdomains')
    miner_res = []
    for resp in response:
        miner_res.append(resp + '.' + query)
    return miner_res


def scan(query):
    print('[-] Searching now in PassiveTotal..')
    pdns_results = passivetotal_get('/v2/enrichment/subdomains', query)
    return pdns_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query
    pdns_results = scan(query)
    for sub in pdns_results:
        print(sub)
