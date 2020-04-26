import dns
import dns.name
import dns.query
import dns.resolver
import argparse

def get_authoritative_nameserver(domain, verbose=False):
    n = dns.name.from_text(domain)

    depth = 2
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]
        if verbose:
            print('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            if verbose:
                print('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            if verbose:
                print('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    return [authority.to_text()[:-1], nameserver]



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    query = args.query
    verbose = True
    author = get_authoritative_nameserver(query, verbose)
    print(author)
