import csv


def check_email(user):
    if "+bootcamp" in user:
        return user
    (name, url) = user.split("@")
    return f"{name}+bootcamp@{url}"


def parse_users(file_name):
    users = {}
    emails = {}

    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            (user, email) = row
            checked_email = check_email(email)
            users[user] = checked_email
            emails[checked_email] = user

    return users, emails
