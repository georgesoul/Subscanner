import requests
import json
import argparse
import socket


def scan(query):
    print('[-] Searching now in BufferDNS..')
    url = "https://dns.bufferover.run/dns?q="+query
    response = requests.request("GET", url)
    dir = str(response.text)
    dir = json.loads(dir)
    results = dir.get('FDNS_A')
    domain = []
    if not results:
        return []
    for i in results:
        info = i.split(',')
        domain.append(info[1])
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
        info = i.split(',')
        count1 += 1
        try:
            ipadress = socket.gethostbyname(str(info[0]))
            print(info[1]+'---'+ipadress)
            count2 += 1
        except:
            print(info[1])
    print('------------------------------------------------------------------\n')
    print('[###]Total unique subdomains discovered: ', count1)
    print('[###]Active subdomains discovered: ', count2)
