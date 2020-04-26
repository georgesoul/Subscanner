import dns
import dns.name
import dns.query
import dns.resolver
import dns.zone
import json
from axfr.get_authoritative_ns import get_authoritative_nameserver
import argparse

def axfr(query):
    author = get_authoritative_nameserver(query)
    try:
        z = dns.zone.from_xfr(dns.query.xfr(author[0], query))
        z= str(z.to_text()).split('\n')
        z= z[0]
        z = z.replace("'", "")
        z = z.replace("\\r", "")
        z= z.split('\\n')
        domain = []
        check = []
        for rec in z:
            if 'IN A' in rec:
                if '@' in rec:
                    if query not in check:
                        rec = rec.split()
                        domain.append([query, rec[-1]])
                        check.append(query)
                        continue
                rec = rec.split()
                if rec[0]+ '.'+ query not in check:
                    domain.append([rec[0] + '.'+ query, rec[-1]])
                    check.append(rec[0] + '.'+ query)
        return domain
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query
    domain = axfr(query)
    if domain:
        for dom in domain:
            print(dom[0]+'---'+dom[1])
