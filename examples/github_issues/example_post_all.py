import os

import requests
from datetime import datetime

from models.qbc.github_issue import GitHubIssue

req_url = 'https://api.github.com/repos/tkutcher/quickbase-client/issues?state=all'
date_fmt = '%Y-%m-%dT%H:%M:%SZ'


def parse_date(date_string):
    return None if date_string is None else \
        datetime.strptime(date_string, date_fmt).date()


response = requests.get(req_url)

issues = []

for item in response.json():
    issue = GitHubIssue(
        issue_id=item['number'],
        title=item['title'],
        description=item['body'],
        labels=','.join([x['name'] for x in item['labels']]),
        date_opened=parse_date(item['created_at']),
        date_closed=parse_date(item['closed_at']),
    )
    issues.append(issue)


client = GitHubIssue.client(os.environ['QB_USER_TOKEN'])

response = client.add_records(issues)
print(response.json())
