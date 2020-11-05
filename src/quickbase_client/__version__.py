
try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version
    try:
        __version__ = version('quickbase_client')
    except PackageNotFoundError:
        __version__ = None
except ModuleNotFoundError:
    __version__ = None

if __name__ == '__main__':
    print(__version__)
