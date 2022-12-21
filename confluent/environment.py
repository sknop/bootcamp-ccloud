import subprocess
import json
import sys


def list_environments():
    environments = {}

    out = subprocess.run("confluent environment list -o json".split(),
                         capture_output=True, universal_newlines=True)
    if out.stderr == '':
        results = json.loads(out.stdout)
        for result in results:
            environments[result['id']] = result['name']
    else:
        print(out.stderr, sys.stderr)

    return environments

