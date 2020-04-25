from pybinaryedge import BinaryEdge
import argparse
import socket


def scan(query):
    print('[-] Searching now in BinaryEdge..')
    be = BinaryEdge('<your_token>')
    results = be.domain_subdomains(query)
    subdom_list = results.get('events')
    return subdom_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    subdomains = scan(query)

    for dom in subdomains:
        print(dom)
