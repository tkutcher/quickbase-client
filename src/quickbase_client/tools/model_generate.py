import os
import sys
from typing import Optional

from quickbase_client.client.api import QuickbaseApiClient
from quickbase_client.orm.field import get_field_type_by_string
from quickbase_client.tools.script import Script
from quickbase_client.utils.pywriting_utils import BasicPyFileWriter
from quickbase_client.utils.pywriting_utils import PyFileWriter
from quickbase_client.utils.pywriting_utils import PyPackageWriter
from quickbase_client.utils.string_utils import id_from_iso_string
from quickbase_client.utils.string_utils import make_unique_var_name
from quickbase_client.utils.string_utils import make_var_name
from quickbase_client.utils.string_utils import parse_realm_and_app_id_from_url


class AppPyFileWriter(PyFileWriter):
    def __init__(self):
        self.pyfile = BasicPyFileWriter()

    def add_header_comments_and_imports(self, app_name, description):
        self.pyfile.add_comment(
            f"app.py - model QuickbaseApp for {app_name} QuickBase App."
        ).add_comment(f"{app_name} - {description}").space().add_line(
            "from quickbase_client.orm.app import QuickbaseApp"
        ).space()

    def add_module_vars(self, version_id):
        self.pyfile.add_line(f"__versionid__ = '{version_id}'").space()

    def add_app_var(self, app_id, app_name, var_name, realm_hostname):
        self.pyfile.add_line(
            f"{var_name} = QuickbaseApp(app_id='{app_id}', name='{app_name}', "
            f"realm_hostname='{realm_hostname}')"
        ).space()

    def get_file_as_string(self):
        return self.pyfile.get_file_as_string()


class TablePyFileWriter(PyFileWriter):
    def __init__(self):
        self.pyfile = BasicPyFileWriter()
        self.field_vars = {}
        self.formula_outlet: Optional[BasicPyFileWriter] = None

    def add_header_comments_and_imports(
        self, app_import_path, app_var_name, file_name, table_name
    ):
        self.pyfile.add_comment(
            f"{file_name}.py - QuickbaseTable for {table_name}"
        ).space().add_line("from quickbase_client import QuickbaseField").add_line(
            "from quickbase_client import QuickbaseFieldType as Qb"
        ).add_line(
            "# from quickbase_client import QuickbaseReport"
        ).add_line(
            "from quickbase_client import QuickbaseTable"
        ).space().add_line(
            f"from {app_import_path}.app import {app_var_name}"
        ).space().space()
        self.formula_outlet = self.pyfile.make_ref()

    def add_table_class_decl(self, table_ident, table_id, app_var_name):
        class_name = make_var_name(table_ident, case="pascal")
        self.pyfile.space().add_line(
            f"class {class_name}(QuickbaseTable):"
        ).indent().add_line(f"__dbid__ = '{table_id}'").add_line(
            f"__app__ = {app_var_name}"
        ).space().add_line(
            "date_created = QuickbaseField(fid=1, field_type=Qb.DATETIME)"
        ).add_line(
            "date_modified = QuickbaseField(fid=2, field_type=Qb.DATETIME)"
        ).add_line(
            "recordid = QuickbaseField(fid=3, field_type=Qb.NUMERIC)"
        ).add_line(
            "record_owner = QuickbaseField(fid=4, field_type=Qb.USER)"
        ).add_line(
            "last_modified = QuickbaseField(fid=5, field_type=Qb.USER)"
        ).space()

    def add_table_field(self, field_name, field_id, field_kind, properties):
        if field_id < 6:
            return  # the special reserved ones already accounted for more or less.
        var_name = make_unique_var_name(field_name, taken=self.field_vars)
        field_kind = str(get_field_type_by_string(field_kind)).split(".")[1]

        formula_str = ""
        if properties["formula"] != "":
            self.formula_outlet.add_line(
                f"{var_name}_formula = '''{properties['formula']}'''"
            ).space()
            formula_str = f", formula={var_name}_formula"

        self.pyfile.add_line(
            f"{var_name} = QuickbaseField("
            f"fid={field_id}, "
            f"field_type=Qb.{field_kind}{formula_str})"
        )

    def done_writing(self):
        self.formula_outlet.space()

    def get_file_as_string(self):
        return self.pyfile.get_file_as_string()


class ModelGenerator(Script):
    registration_name = "model-generate"

    def __init__(
        self, realm_hostname, app_id, user_token, pkg_dir=None, table_ids=None
    ):
        self.realm_hostname = realm_hostname
        self.app_id = app_id
        self.user_token = user_token
        self.app_var_name = None
        self.table_vars = {}
        self.pkg_import_stmt = ""
        self.table_ids = table_ids if table_ids else []

        if pkg_dir is None:
            models_pkg = PyPackageWriter(pkg_name="models", parent_dir=os.getcwd())
            if not os.path.exists(models_pkg.pkg_path):
                models_pkg.write()
            pkg_dir = models_pkg.pkg_path
            self.pkg_import_stmt = "models"

        self.pkg_writer = PyPackageWriter(pkg_name="PLACEHOLDER", parent_dir=pkg_dir)

    @staticmethod
    def add_argparse_args(parser):
        parser.add_argument(
            "-a",
            "--app-url",
            nargs="?",
            required=True,
            help="the URL of the home page of the app",
        )
        parser.add_argument(
            "-d",
            "--pkg-dir",
            nargs="?",
            default=None,
            help='the directory to put the package in, defaults to "models"',
        )
        parser.add_argument(
            "-t",
            "--user-tok",
            nargs="?",
            default=None,
            help="the user token to authenticate - if not provided will read from "
            "environment variable QB_USER_TOKEN",
        )
        parser.add_argument(
            "-i",
            "--include",
            nargs="?",
            default=None,
            action="append",
            help="ID or name of a table to include - can be specified "
            "multiple times; if present, excludes all other tables",
        )

    @staticmethod
    def instantiate_from_ns(ns) -> "Script":
        realm_hostname, app_id = parse_realm_and_app_id_from_url(ns.app_url)
        try:
            user_tok = (
                ns.user_tok if ns.user_tok is not None else os.environ["QB_USER_TOKEN"]
            )
            return ModelGenerator(
                realm_hostname,
                app_id,
                user_token=user_tok,
                pkg_dir=ns.pkg_dir,
                table_ids=ns.include,
            )
        except (KeyError, OSError):
            raise EnvironmentError(
                "ERROR: expected either a -t argument or a "
                "QB_USER_TOKEN environment variable"
            )

    def add_app_file(self, app_data):
        name = app_data["name"]
        self.pkg_writer.pkg_name = make_var_name(name, case="snake")
        self.pkg_import_stmt += (
            "." if self.pkg_import_stmt else ""
        ) + self.pkg_writer.pkg_name
        description = app_data["description"]
        updated = app_data["updated"]
        versionid = id_from_iso_string(updated)
        self.app_var_name = make_var_name(name, case="pascal")
        w = AppPyFileWriter()
        w.add_header_comments_and_imports(app_name=name, description=description)
        w.add_module_vars(versionid)
        w.add_app_var(self.app_id, name, self.app_var_name, self.realm_hostname)
        self.pkg_writer.add_module("app", w)

    def add_table_file(self, table, fields):
        table_ident = table["singleRecordName"]
        file_name = make_var_name(table_ident)
        if file_name in self.pkg_writer.modules:
            table_ident = table["alias"].replace("_DBID_", "")
            file_name = make_var_name(table_ident)
        w = TablePyFileWriter()
        w.add_header_comments_and_imports(
            self.pkg_import_stmt, self.app_var_name, file_name, table["name"]
        )
        w.add_table_class_decl(table_ident, table["id"], self.app_var_name)
        for f in sorted(fields, key=lambda f: int(f["id"])):
            w.add_table_field(f["label"], f["id"], f["fieldType"], f["properties"])
        w.done_writing()
        self.pkg_writer.add_module(file_name, w)

    def run(self):
        api = QuickbaseApiClient(
            user_token=self.user_token, realm_hostname=self.realm_hostname
        )

        app_data = api.get_app(self.app_id)
        if not app_data.ok:
            if "invalid dbid" in app_data.json()["message"].lower():
                sys.stderr.write(
                    "URL should be to the app home page, not a specific table.\n"
                )
                return False
            else:
                sys.stderr.write(app_data.text + "\n")
                raise ValueError(
                    f"received {app_data.status_code} from QuickBase API -"
                    f"see error log above"
                )
        self.add_app_file(app_data.json())

        tables = api.get_tables_for_app(self.app_id)
        for table in tables.json():
            table_id = table["id"]
            table_ident = table["singleRecordName"]
            table_var = make_var_name(table_ident)
            if not len(self.table_ids) or any(
                x in self.table_ids for x in [table_var, table_ident, table_id]
            ):
                # if not table_ids have been specified, or they have but this table's ID,
                # single record name, or var name are in the list, generate it
                fields = api.get_fields_for_table(table_id)
                self.add_table_file(table, fields.json())

        self.pkg_writer.write()
        return True
