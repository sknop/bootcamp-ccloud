import json
import subprocess
import sys


def list_ksql_clusters(environment):
    result = []

    out = subprocess.run(f"confluent ksql cluster list --environment {environment} -o json".split(),
                         capture_output=True, universal_newlines=True)
    if out.stderr == '':
        ksql_clusters = json.loads(out.stdout)
        for ksql_cluster in ksql_clusters:
            result.append(ksql_cluster["id"])
    else:
        print(out.stderr, file=sys.stdout)

    return result
