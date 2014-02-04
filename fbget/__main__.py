#!/usr/bin/env python2

from .auth import getCredentials
from .graphapi import GraphAPI, PhotoSync
from pprint import pprint
import logging


def parse_args():
    import argparse
    p = argparse.ArgumentParser(add_help=False)
    # oauth2client required options
    p.add_argument('--auth_host_name', default='localhost',
                   help='Hostname when running a local web server.')
    p.add_argument('--noauth_local_webserver', action='store_true',
                   default=False, help='Do not run a local web server.')
    p.add_argument('--auth_host_port', default=[8080, 8090], type=int,
                   nargs='*', help='Port web server should listen on.')
    p.add_argument('--logging_level', default='ERROR',
                   choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                   help='Set the logging level of detail.')
    # secret related options
    p.add_argument('--secrets', metavar='<secrets.json>', required=True)
    p.add_argument('--tokens', metavar='<tokens-file>', required=True)
    p.add_argument('--outdir', required=True)
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.logging_level)
    scopes = ','.join(['user_photos'])
    cred = getCredentials(args.secrets, args.tokens, scopes, args)

    gapi = GraphAPI(cred)
    tagged = gapi.photos()
    PhotoSync(cred, args.outdir, tagged).sync()


if __name__ == '__main__':
    main()
