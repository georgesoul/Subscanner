import dns.resolver
import requests
from threading import Thread
from queue import Queue
import socket
import argparse
import time
import os
from requests.packages.urllib3.contrib import pyopenssl as reqs
from sublister import sublist3r
from services import Fb, Binaryedge, CertSpotter, Bufferdns, ThreatMiner, HackerTarget, PassiveTotal
from axfr import zone_transfer_axfr, get_authoritative_ns
import pandas as pd

global q, wildcards

q = Queue()
'''
#attempt transfer zone
def axfr(domain):
    try:
      res = dns.resolver.query(domain, 'SOA')
    except:
      pass
    else:
      for soa in res:
          soa = str(soa.to_text()).split(" ", 1)[0]
          ipadress = socket.gethostbyname(soa)
      dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
      dns.resolver.default_resolver.nameservers = [ipadress]
    try:
        results = dns.resolver.query(domain, 'AXFR')
    except:
        return 0
    else:
        for subdomains in results:
            print(subdomains.to_text())
        return 1
'''

#extract subdomain names from ssl/tls certificate
def https_cert_subject_alt_names(host, port):
    try:
       x509 = reqs.OpenSSL.crypto.load_certificate(
           reqs.OpenSSL.crypto.FILETYPE_PEM,
           reqs.ssl.get_server_certificate((host, port))
       )
       return reqs.get_subj_alt_name(x509)
    except:
       return


#brute force
def find_active(domain):
    global wildcards
    #domain_ip = socket.gethostbyname(domain)
    while True:
        subdomain = q.get()
        url = f"http://{subdomain}.{domain}"
        try:
            r = requests.get(url)
            #print(r.status_code)
        except requests.ConnectionError:
            pass
        else:
            if (r.status_code != 404 and (not (socket.gethostbyname(f"{subdomain}.{domain}")) in wildcards)):
                #if (f"{subdomain}.{domain}" not in sublist):
                    print(f"{subdomain}.{domain}")
        q.task_done()



def brute_force(domain, threads, subdomains):
    st = time.time()
    for subdomain in subdomains:
        q.put(subdomain)
    en = time.time()
    print(en-st)
    for t in range(threads):
        scanner = Thread(target=find_active, args=(domain,))
        scanner.daemon = True
        scanner.start()


def lookup(domain):
    try:
        res = dns.resolver.query(domain, 'A')
        return res
    except:
        return


def get_active_IPs(sublist):
    report_list = []
    for subdomain in sublist:
        try:
            report_list.append([subdomain, socket.gethostbyname(str(subdomain))])
        except:
            report_list.append([subdomain, 'INACTIVE'])
    return report_list


def return_report(report_list, domain):
    df = pd.DataFrame(report_list, columns=['Subdomain', 'IP_address'])
    report_to_excel = pd.ExcelWriter(domain+'.xlsx', engine='xlsxwriter')
    df.to_excel(report_to_excel, sheet_name='Sheet1')
    report_to_excel.save()


if __name__ == '__main__':
    global wildcards
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('-b', '--bruteforce', nargs='?', default=False)
    parser.add_argument('-o', '--output', nargs='?', default=False)
    args = parser.parse_args()
    domain = args.domain
    enable_bruteforce = args.bruteforce
    give_report = args.output
    threads = 20

    print("[-] Enumerating subdomains now for %s" % domain)
    startTime = time.time()
    report_list = []
    report_list = zone_transfer_axfr.axfr(domain)
    if not report_list:
        wildcards = []
        systime = str(int(time.time()))
        try:
            response = lookup("a" + systime + "." + domain)
        except:
            pass
        if (response):
           for data in response:
               address = data.address
               wildcards.append(address)
               print("[-] Wildcard IP found: "  + address)
        else:
               print("[-] No wildcard exist")

        sublist = []

        fb = Fb.scan(domain)
        if (fb):
            sublist = sublist + fb

        binaryedge = Binaryedge.scan(domain)
        if (binaryedge):
            sublist = sublist + binaryedge

        certspotter = CertSpotter.scan(domain)
        if (certspotter):
            sublist = sublist + certspotter

        bufferdns = Bufferdns.scan(domain)
        if (bufferdns):
            sublist = sublist + bufferdns

        threatminer = ThreatMiner.scan(domain)
        if (threatminer):
            sublist = sublist + threatminer

        hackertarget = HackerTarget.scan(domain)
        if (hackertarget):
            sublist = sublist + hackertarget

        passivetotal = PassiveTotal.scan(domain)
        if (passivetotal):
            sublist = sublist + passivetotal

        sublistr = sublist3r.main(domain, threads, savefile = False, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
        if (sublistr):
            sublist = sublist + sublistr

        cert = https_cert_subject_alt_names(domain, 443)
        if (cert):
            for subd in cert:
                if (subd[1] not in sublist):
                    sublist.append(subd[1])


        sublist = list(set(sublist))

        counter_unique = 0
        if(sublist):
           for sub in sublist:
               counter_unique += 1
               print(sub)

        if enable_bruteforce:
            brute_force(domain=domain, threads=threads, subdomains=open('subdomains_small.txt').read().splitlines())
            q.join()

        endTime = time.time()
        enumerationTime =  endTime - startTime
        print('#####################################################################################')
        print('[-] %d unique subdomains discovered in %d seconds' % (counter_unique, enumerationTime))
        report_list =  get_active_IPs(sublist)
    return_report(report_list, domain)
