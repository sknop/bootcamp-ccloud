import argparse
import subprocess

from confluent import list_environments, list_invitations, list_clusters, list_connectors, list_ksql_clusters
from parse_users import parse_users


class DeleteUsers:
    def __init__(self, filename, delete_all=False):
        self.environments = {}
        self.uids = {}
        self.users = {}
        self.emails = {}
        self.clusters = {}
        self.ksql_clusters = {}
        self.connectors = {}
        self.file_name = filename
        self.delete_all = delete_all

    def process(self):
        # list environments
        # list all clusters for each environment
        # list invites

        # breakpoint()

        self.parse_users()
        self.list_environments()
        self.list_clusters()
        self.list_connectors()
        self.list_ksql_clusters()
        self.list_invites()

        self.delete_environments()
        self.delete_invites()

    def list_environments(self):
        self.environments = list_environments()
        for identifier, name in self.environments.items():
            print(f"{identifier} : {name}")

    def list_clusters(self):
        for environment in self.environments.keys():
            self.clusters[environment] = list_clusters(environment)
            print(f"{environment} : {self.clusters[environment]}")

    def list_invites(self):
        self.uids = list_invitations()
        for email, name in self.uids.items():
            print(f"{email} : {name}")

    def list_connectors(self):
        for environment in self.environments.keys():
            for cluster in self.clusters[environment]:
                self.connectors[cluster] = list_connectors(environment, cluster)
                print(f"{self.connectors[cluster]}")

    def list_ksql_clusters(self):
        for environment in self.environments.keys():
            self.ksql_clusters[environment] = list_ksql_clusters(environment)

    def parse_users(self):
        self.users, self.emails = parse_users(self.file_name)
        for user, email in self.users.items():
            print(f"User = {user}, email = {email}")

    def delete_connectors(self, environment, cluster):
        for connect in self.connectors[cluster]:
            print(f"Delete connector {connect}")
            out = subprocess.run(
                f"confluent connect cluster delete --force --cluster {cluster} --environment {environment} {connect}".split(),
                capture_output=True, universal_newlines=True)
            if out.stderr != '':
                print(out.stderr)

    def delete_clusters(self, environment):
        for cluster in self.clusters[environment]:
            print(f"Deleting cluster {cluster}")
            self.delete_connectors(environment, cluster)
            out = subprocess.run(f"confluent kafka cluster delete --force {cluster} --environment {environment}".split(),
                                 capture_output=True, universal_newlines=True)
            if out.stderr != '':
                print(out.stderr)

    def delete_environments(self):
        for user in self.users.keys():
            print(f"Deleting user {user}")
            envs = [env for env, name in self.environments.items() if name == user]
            if len(envs) > 0:
                env = envs[0]
                print(f"Deleting environment {env}")
                self.delete_ksql_clusters(env)
                self.delete_clusters(env)
                out = subprocess.run(f"confluent environment delete --force {env}".split(),
                                     capture_output=True, universal_newlines=True)
                if out.stderr != '':
                    print(out.stderr)

    def delete_ksql_clusters(self, env):
        for ksql_cluster in self.ksql_clusters[env]:
            print(f"Deleting ksql cluster {ksql_cluster}")
            out = subprocess.run(f"confluent ksql cluster delete --force {ksql_cluster} --environment {env}".split(),
                                 capture_output=True, universal_newlines=True)
            if out.stderr != '':
                print(out.stderr)

    def delete_invites(self):
        to_delete = []

        for email, uid in self.uids.items():
            if not self.delete_all:
                # verify user is in target list
                if email in self.emails:
                    to_delete.append(uid)
            else:
                to_delete.append(uid)

        for uid in to_delete:
            print(f"Deleting user {uid}")
            out = subprocess.run(f"confluent iam user delete {uid}".split(),
                                 capture_output=True, universal_newlines=True)
            if out.stderr != '':
                print(out.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Delete CCloud Users",
                                     description="Removes users and their resources")
    parser.add_argument('filename')
    parser.add_argument('-d', '--delete-all', action='store_true')

    args = parser.parse_args()
    prog = DeleteUsers(args.filename, args.delete_all)
    prog.process()
