from importlib.metadata import version

try:
    __version__ = version('quickbase_client')
except:
    __version__ = 'unknown'


if __name__ == '__main__':
    print(__version__)
