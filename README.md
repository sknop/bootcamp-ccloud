# bootcamp-ccloud
Infrastructure for day 1 of the CC bootcamp

## Requirement:
- `confluent` CLI installed
- logged into the CCloud instance where the users will be invited and their environments created
- a CSV file with usernames and their emails in the form 

  name,email

## Actions performed

- Add `+bootcamp` to the email name before the `@` if not there already
- Send an invitation to every user in the CSV file
- Collect a list of all invites and harvest the user ids of the users in the CSV file
- Create an environment for each user
- Assign each user to be the EnvironmentAdmin of his/her environment

Two bypasses exist that can be used individually or together:

- `--skip-invite`: Do not send the invite (most likely because something went wrong before and the user is already invited
- `--skip-environments`: Do not create the environments (same reason as above), instead all environments are listed and attached to the user

```
usage: Create CCloud Users [-h] [-s] [-e] filename

Invites users to CCloud instance, creates environments and assigns roles

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -s, --skip-invite
  -e, --skip-environments
```
