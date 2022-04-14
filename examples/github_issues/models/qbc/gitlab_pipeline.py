# git_lab_pipeline.py - QuickbaseTable for GitLab Pipelines

from quickbase_client import QuickbaseField
from quickbase_client import QuickbaseFieldType as Qb

# from quickbase_client import QuickbaseReport
from quickbase_client import QuickbaseTable

from models.qbc.app import Qbc


class GitLabPipeline(QuickbaseTable):
    __dbid__ = "bqyqauine"
    __app__ = Qbc

    date_created = QuickbaseField(fid=1, field_type=Qb.DATETIME)
    date_modified = QuickbaseField(fid=2, field_type=Qb.DATETIME)
    recordid = QuickbaseField(fid=3, field_type=Qb.NUMERIC)
    record_owner = QuickbaseField(fid=4, field_type=Qb.USER)
    last_modified = QuickbaseField(fid=5, field_type=Qb.USER)

    url = QuickbaseField(fid=6, field_type=Qb.OTHER)
    date = QuickbaseField(fid=7, field_type=Qb.DATE)
    duration = QuickbaseField(fid=8, field_type=Qb.DURATION)
    passed = QuickbaseField(fid=9, field_type=Qb.CHECKBOX)
