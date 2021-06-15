====================
CLI Tools
====================


This package includes a simple command line utility ``qbc`` for running scripts.

The primary script is `model-generate` which can be used to generate the specific model
classes.

The main program itself has one command (run) which can be used to run any scripts that
are registered with it (the only core one being model-generate right now).

The ``--show-stacktrace`` flag will re-raise any errors (internal) that may have occurred.

.. code-block::

    $ qbc -h
    usage: qbc [-h] [--show-stacktrace] {run} ...

    positional arguments:
      {run}              command help
        run              run a script.

    optional arguments:
      -h, --help         show this help message and exit
      --show-stacktrace


Running ``model-generate`` you can pass your user token on the command line or set the
``QB_USER_TOKEN`` environment variable.

.. code-block::

    $ qbc run model-generate -h
    usage: qbc run model-generate [-h] -a [APP_URL] [-d [PKG_DIR]] [-t [USER_TOK]] [-i [INCLUDE]]

    optional arguments:
      -h, --help            show this help message and exit
      -a [APP_URL], --app-url [APP_URL]
                            the URL of the home page of the app
      -d [PKG_DIR], --pkg-dir [PKG_DIR]
                            the directory to put the package in, defaults to "models"
      -t [USER_TOK], --user-tok [USER_TOK]
                            the user token to authenticate - if not provided will read from
                            environment variable QB_USER_TOKEN
      -i [INCLUDE], --include [INCLUDE]
                            ID or name of a table to include - can be specified
                            multiple times; if present, excludes all other tables
