import json
import subprocess
import sys


def list_connectors(environment, cluster):
    result = []

    out = subprocess.run(f"confluent connect list --environment {environment} --cluster {cluster} -o json".split(),
                         capture_output=True, universal_newlines=True)
    if out.stderr == '':
        connectors = json.loads(out.stdout)
        for connector in connectors:
            result.append(connector["id"])
    else:
        print(out.stderr, file=sys.stdout)

    return result
