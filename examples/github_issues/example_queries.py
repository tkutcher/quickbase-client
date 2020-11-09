import os
from datetime import date

from quickbase_client.query import or_
from quickbase_client.query import and_
from quickbase_client.query import contains_
from quickbase_client.query import lt_
from quickbase_client.query import on_or_before_

from models.qbc.github_issue import GitHubIssue

schema = GitHubIssue.schema
client = GitHubIssue.client(os.environ['QB_USER_TOKEN'])

all_bugs_query = contains_(schema.labels, 'bug')

recs = client.query(all_bugs_query)
print([str(r) for r in recs])

complex_query = or_(
    all_bugs_query,
    and_(
        lt_(schema.issue_id, 14),
        on_or_before_(schema.date_closed, date(year=2020, month=11, day=1))
    )
)

print(complex_query.where)
recs = client.query(complex_query)

for r in recs:
    print(str(r))
