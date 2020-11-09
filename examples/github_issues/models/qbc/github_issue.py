# git_hub_issue.py - QuickBaseTable for GitHub Issues

from quickbase_client import QuickBaseField
from quickbase_client import QuickBaseFieldType as Qb
# from quickbase_client import QuickBaseReport
from quickbase_client import QuickBaseTable

from models.qbc.app import Qbc


is_open_formula = 'IsNull([Date Closed])'

issue_url_formula = '"https://github.com/tkutcher/quickbase-client/issues/"&[Issue ID]'

class GitHubIssue(QuickBaseTable):
    __dbid__ = 'bqyqaqrb9'
    __app__ = Qbc
    
    date_created = QuickBaseField(fid=1, field_type=Qb.DATETIME)
    date_modified = QuickBaseField(fid=2, field_type=Qb.DATETIME)
    recordid = QuickBaseField(fid=3, field_type=Qb.NUMERIC)
    record_owner = QuickBaseField(fid=4, field_type=Qb.USER)
    last_modified = QuickBaseField(fid=5, field_type=Qb.USER)
    
    title = QuickBaseField(fid=6, field_type=Qb.TEXT)
    description = QuickBaseField(fid=7, field_type=Qb.TEXT_MULTILINE)
    issue_id = QuickBaseField(fid=8, field_type=Qb.NUMERIC)
    date_opened = QuickBaseField(fid=9, field_type=Qb.DATE)
    date_closed = QuickBaseField(fid=10, field_type=Qb.DATE)
    labels = QuickBaseField(fid=11, field_type=Qb.TEXT_MULTILINE)
    is_open = QuickBaseField(fid=12, field_type=Qb.CHECKBOX, formula=is_open_formula)
    issue_url = QuickBaseField(fid=13, field_type=Qb.OTHER, formula=issue_url_formula)

    def __str__(self):
        return f'<GitHubIssue #{int(self.issue_id)} "{self.title}">'
