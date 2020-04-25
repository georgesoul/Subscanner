import requests
import json
import argparse
import socket


def scan(query):
    print('[-] Searching now in HackerTarget..')
    url = "https://api.hackertarget.com/hostsearch/?q=" + query
    response = requests.request("GET", url)
    dir = str(response.text).splitlines()
    domain = []
    for res in dir:
        res = res.split(',')[0]
        domain.append(res)
    return domain

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    domain = scan(query)

    count1 = 0
    count2 = 0
    for i in domain:
        count1 += 1
        try:
            ipadress = socket.gethostbyname(str(i))
            print(i+'---'+ipadress)
            count2 += 1
        except:
            print(i)
    print('------------------------------------------------------------------\n')
    print('[###]Total unique subdomains discovered: ', count1)
    print('[###]Active subdomains discovered: ', count2)
