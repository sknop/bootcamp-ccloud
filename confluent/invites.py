import json
import subprocess
import sys


def list_invitations():
    uids = {}

    out = subprocess.run("confluent iam user invitation list -o json".split(),
                         capture_output=True, universal_newlines=True)
    if out.stderr == '':
        invites = json.loads(out.stdout)
        for invite in invites:
            uids[invite['email']] = invite['id']
    else:
        print(out.stderr, file=sys.stdout)

    return uids
