# git_lab_pipeline.py - QuickBaseTable for GitLab Pipelines

from quickbase_client import QuickBaseField
from quickbase_client import QuickBaseFieldType as Qb
# from quickbase_client import QuickBaseReport
from quickbase_client import QuickBaseTable

from models.qbc.app import Qbc



class GitLabPipeline(QuickBaseTable):
    __dbid__ = 'bqyqauine'
    __app__ = Qbc
    
    date_created = QuickBaseField(fid=1, field_type=Qb.DATETIME)
    date_modified = QuickBaseField(fid=2, field_type=Qb.DATETIME)
    recordid = QuickBaseField(fid=3, field_type=Qb.NUMERIC)
    record_owner = QuickBaseField(fid=4, field_type=Qb.USER)
    last_modified = QuickBaseField(fid=5, field_type=Qb.USER)
    
    url = QuickBaseField(fid=6, field_type=Qb.OTHER)
    date = QuickBaseField(fid=7, field_type=Qb.DATE)
    duration = QuickBaseField(fid=8, field_type=Qb.DURATION)
    passed = QuickBaseField(fid=9, field_type=Qb.CHECKBOX)