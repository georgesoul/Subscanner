from spyse import spyse
import argparse
import socket

def scan(query):
    s = spyse()
    subdomains = s.subdomains(query, param="domain")
    subdomains = subdomains.get('records')
    domain = []
    for i in subdomains:
        dom = i.get('domain')
        domain.append(dom)
        print(dom)
    '''
        try:
            ip = i.get('ip')
            an = ip.get('as_number')
            org = an.get('organization')
        except:
            org = 'Unknown'
        print(dom,org)
    '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    miner_res = scan(query)
