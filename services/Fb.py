import requests
import json
import argparse
import socket

def scan(query):
    print('[-] Searching now in Facebook..')
    url = "https://graph.facebook.com/certificates?query="+query+"&fields=domains&limit=20000"
    querystring = {"access_token": '<your_token>'}
    response = requests.request("GET", url, params=querystring)
    dir = str(response.text)
    dir = json.loads(dir)
    domain = dir.get('data')
    fb_res = []
    for i in domain:
        dom = i.get('domains')
        for j in dom:
            fb_res.append(j)

    fb_res = list(set(fb_res))
    return fb_res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query

    fb_result = scan(query)

    count1 = 0
    count2 = 0
    for i in fb_result:
        count1 += 1
        try:
            ipadress = socket.gethostbyname(str(i))
            print(i+'---'+ipadress)
            count2 += 1
        except:
            print(i)

    print('\n\n')
    print('[###]Total unique subdomains discovered: ', count1)
    print('[###]Active subdomains discovered: ', count2)
