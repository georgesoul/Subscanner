import requests
import json
import argparse
import socket


def scan(query):
    print('[-] Searching now in CertSpotter..')
    url = "https://api.certspotter.com/v1/issuances?domain="+query+"&include_subdomains=true&expand=dns_names"
    response = requests.request("GET", url)
    dir = str(response.text)
    dir = json.loads(dir)
    miner_res = []
    for data in dir:
        names = data.get('dns_names')
        for domain in names:
            miner_res.append(domain)

    miner_res = list(set(miner_res))
    return miner_res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    miner_res = scan(query)

    count1 = 0
    count2 = 0

    for domain in miner_res:
        count1 += 1
        try:
            ipadress = socket.gethostbyname(str(domain))
            print(domain+'---'+ipadress)
            count2 += 1
        except:
            print(domain)
    print('------------------------------------------------------------------\n')
    print('[###]Total unique subdomains discovered: ', count1)
    print('[###]Active subdomains discovered: ', count2)
