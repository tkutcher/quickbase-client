# git_hub_issue.py - QuickbaseTable for GitHub Issues

from quickbase_client import QuickbaseField
from quickbase_client import QuickbaseFieldType as Qb

# from quickbase_client import QuickbaseReport
from quickbase_client import QuickbaseTable

from models.qbc.app import Qbc


is_open_formula = "IsNull([Date Closed])"

issue_url_formula = '"https://github.com/tkutcher/quickbase-client/issues/"&[Issue ID]'


class GitHubIssue(QuickbaseTable):
    __dbid__ = "bqyqaqrb9"
    __app__ = Qbc

    date_created = QuickbaseField(fid=1, field_type=Qb.DATETIME)
    date_modified = QuickbaseField(fid=2, field_type=Qb.DATETIME)
    recordid = QuickbaseField(fid=3, field_type=Qb.NUMERIC)
    record_owner = QuickbaseField(fid=4, field_type=Qb.USER)
    last_modified = QuickbaseField(fid=5, field_type=Qb.USER)

    title = QuickbaseField(fid=6, field_type=Qb.TEXT)
    description = QuickbaseField(fid=7, field_type=Qb.TEXT_MULTILINE)
    issue_id = QuickbaseField(fid=8, field_type=Qb.NUMERIC)
    date_opened = QuickbaseField(fid=9, field_type=Qb.DATE)
    date_closed = QuickbaseField(fid=10, field_type=Qb.DATE)
    labels = QuickbaseField(fid=11, field_type=Qb.TEXT_MULTILINE)
    is_open = QuickbaseField(fid=12, field_type=Qb.CHECKBOX, formula=is_open_formula)
    issue_url = QuickbaseField(fid=13, field_type=Qb.OTHER, formula=issue_url_formula)

    def __str__(self):
        return f'<GitHubIssue #{int(self.issue_id)} "{self.title}">'
