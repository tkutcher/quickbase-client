# app.py - model QuickbaseApp for QBC QuickBase App.
# QBC -

from quickbase_client.orm.app import QuickbaseApp

__versionid__ = "20201106030637"

Qbc = QuickbaseApp(
    app_id="bqyhichwa",
    name="QBC",
    realm_hostname="builderprogram-tkutcher.quickbase.com",
)
