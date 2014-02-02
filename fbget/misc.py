#!/usr/bin/env python2

# little hack for certs not found
import httplib2
ca_certs="/etc/ssl/certs/ca-certificates.crt"

def Http(*args, **kwargs):
    return httplib2.Http(ca_certs=ca_certs, *args, **kwargs)
