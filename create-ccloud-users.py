import argparse
import sys
import csv
import subprocess
import json


def check_email(user):
    if "+bootcamp" in user:
        return user
    (name, url) = user.split("@")
    return f"{name}+bootcamp@{url}"


class CreateUsers:
    def __init__(self, file_name, skip_invites=False, skip_environments=False):
        self.file_name = file_name
        self.users = {}
        self.emails = {}
        self.environments = {}
        self.uids = {}
        self.skip_invites = skip_invites
        self.skip_environments = skip_environments

    def process(self):
        self.parse_users()
        if not self.skip_invites:
            self.invite_users()
        self.list_invites()
        if self.skip_environments:
            self.list_environments()
        else:
            self.create_environments()
        self.assign_environment_to_user()

    def parse_users(self):
        with open(self.file_name) as f:
            reader = csv.reader(f)
            for row in reader:
                (user, email) = row
                checked_email = check_email(email)
                self.users[user] = checked_email
                self.emails[checked_email] = user
                print(f"User = {user}, email = {checked_email}")

    def invite_users(self):
        for user, email in self.users.items():
            cmd = f"confluent iam user invitation create {email}"
            print(cmd)
            args = cmd.split()
            out = subprocess.run(args, capture_output=True, universal_newlines=True)
            print(out.stdout)
            if out.stderr != '':
                print(out.stderr, sys.stderr)

    def list_invites(self):
        out = subprocess.run("confluent iam user invitation list -o json".split(),
                             capture_output=True, universal_newlines=True)
        if out.stderr == '':
            invites = json.loads(out.stdout)
            for invite in invites:
                self.uids[invite['email']] = invite['user_resource_id']
                print(f"{invite['email']} : {invite['user_resource_id']}")
        else:
            print(out.stderr, file=sys.stdout)

    def create_environments(self):
        for user in self.users.keys():
            out = subprocess.run(f"confluent environment create {user} -o json".split(),
                                 capture_output=True, universal_newlines=True)
            if out.stderr == '':
                result = json.loads(out.stdout)
                self.environments[result['id']] = user
            else:
                print(out.stderr)

    def list_environments(self):
        out = subprocess.run("confluent environment list -o json".split(),
                             capture_output=True, universal_newlines=True)
        if out.stderr == '':
            results = json.loads(out.stdout)
            for result in results:
                self.environments[result['id']] = result['name']
                print(f"{result['id']} : {result['name']}")

    def assign_environment_to_user(self):
        for env, user in self.environments.items():
            if user in self.users:
                email = self.users[user]
                user_id = self.uids[email]
                cmd = f"confluent iam rbac role-binding create --principal User:{user_id} --role EnvironmentAdmin --environment {env}"
                out = subprocess.run(cmd.split(), capture_output=True,universal_newlines=True)
                if out.stderr != '':
                    print(out.stderr, sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Create CCloud Users",
        description="Invites users to CCloud instance, creates environments and assigns roles")
    parser.add_argument('filename')
    parser.add_argument('-s', '--skip-invite', action='store_true')
    parser.add_argument('-e', '--skip-environments', action='store_true')

    args = parser.parse_args()

    create_user = CreateUsers(args.filename, args.skip_invite, args.skip_environments)

    create_user.process()

