#!/usr/bin/env python2

from oauth2client.tools import run_flow
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

from .misc import Http


def getCredentials(secrets_file, tokens_file, scopes, flags):
    # create an auth flow in case we need to authenticate
    auth_flow = flow_from_clientsecrets(secrets_file, scope=scopes,
                                        message="Visit the APIs Console")
    # search for existing tokens
    storage = Storage(tokens_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        run_flow(auth_flow, storage, flags, Http())
    return credentials
