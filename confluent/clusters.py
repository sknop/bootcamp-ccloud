import json
import subprocess
import sys


def list_clusters(environment):
    result = {}

    out = subprocess.run(f"confluent kafka cluster list --environment {environment} -o json".split(),
                         capture_output=True, universal_newlines=True)
    if out.stderr == '':
        clusters = json.loads(out.stdout)
        for cluster in clusters:
            result[cluster['id']] = cluster
    else:
        print(out.stderr, file=sys.stdout)

    return result
