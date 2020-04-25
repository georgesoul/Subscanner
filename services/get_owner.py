import requests
import json
import argparse
import socket


def scan(query):
    print('[-] Searching now in HackerTarget..')
    url = "https://api.hackertarget.com/whois/?q=" + query
    response = requests.request("GET", url)
    dir = str(response.text).splitlines()
    #print(dir)
    domain = []
    mail = dir[11].split()[-1]
    mail = mail.replace("'", "")
    org = dir[-8].split()[-1]
    print(mail)
    print(org)
    '''
    for res in dir:
        #res = res.split(',')[0]
        #domain.append(res)
        print(res)
        '''
    return dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    domain = scan(query)
