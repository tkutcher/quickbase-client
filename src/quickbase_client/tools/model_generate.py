import os

from quickbase_client.client.api import QuickBaseApiClient
from quickbase_client.tools.script import Script
from quickbase_client.utils.pywriting_utils import BasicPyFileWriter
from quickbase_client.utils.pywriting_utils import PyFileWriter
from quickbase_client.utils.pywriting_utils import PyPackageWriter
from quickbase_client.utils.string_utils import id_from_iso_string
from quickbase_client.utils.string_utils import make_var_name


class AppPyFileWriter(PyFileWriter):

    def __init__(self):
        self.pyfile = BasicPyFileWriter()

    def add_header_comments_and_imports(self, app_name, description):
        self.pyfile.add_comment(f'app.py - model QuickBaseApp for {app_name} QuickBase App.')\
            .add_comment(f'{app_name} - {description}')\
            .space()\
            .add_line('from quickbase_client.orm.app import QuickBaseApp').space()

    def add_module_vars(self, version_id):
        self.pyfile.add_line(f"__versionid__ = '{version_id}'").space()

    def add_app_var(self, app_id, app_name, var_name, realm_hostname):
        self.pyfile.add_line(
            f"{var_name} = QuickBaseApp(app_id='{app_id}', name='{app_name}', "
            f"realm_hostname='{realm_hostname}')")

    def get_file_as_string(self):
        return self.pyfile.get_file_as_string()


class ModelGenerator(Script):

    def __init__(self, realm_hostname, user_token, app_id, pkg_dir=None):
        self.realm_hostname = realm_hostname
        self.user_token = user_token
        self.app_id = app_id

        if pkg_dir is None:
            models_pkg = PyPackageWriter(pkg_name='models', parent_dir=os.getcwd())
            if not os.path.exists(models_pkg.pkg_path):
                models_pkg.write()
            pkg_dir = models_pkg.pkg_path

        self.pkg_writer = PyPackageWriter(pkg_name='PLACEHOLDER', parent_dir=pkg_dir)

    def add_app_file(self, app_data):
        name = app_data['name']
        self.pkg_writer.pkg_name = make_var_name(name, case='snake')
        description = app_data['description']
        updated = app_data['updated']
        versionid = id_from_iso_string(updated)
        var_name = make_var_name(name, case='pascal')
        w = AppPyFileWriter()
        w.add_header_comments_and_imports(app_name=name, description=description)
        w.add_module_vars(versionid)
        w.add_app_var(self.app_id, name, var_name, self.realm_hostname)
        self.pkg_writer.add_module('app', w)

    def run(self):
        api = QuickBaseApiClient(user_token=self.user_token, realm_hostname=self.realm_hostname)

        app_data = api.get_app(self.app_id)
        self.add_app_file(app_data.json())

        # tables = api.get_tables_for_app(self.app_id)
        # for table in tables.json():
        #     table_id = table['id']
        #     fields = api.get_fields_for_table(table_id)
        #     print(fields.json())

        self.pkg_writer.write()


if __name__ == '__main__':
    tok = os.getenv('QB_USER_TOKEN')
    gen = ModelGenerator(realm_hostname='dicorp.quickbase.com',
                         user_token=tok,
                         app_id='bqxuhmrkw')
    gen.run()
