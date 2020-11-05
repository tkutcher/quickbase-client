import argparse
import sys

from quickbase_client.tools.script_loader import CoreScriptLoader

scripts = CoreScriptLoader().load_scripts()


def _run(ns):
    print('running...')
    script_instance = ns.script_cls.instantiate_from_ns(ns)
    if script_instance:
        retval = script_instance.run()
        if retval:
            print('done!')
        return retval
    else:
        return 1


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--show-stacktrace', action='store_true')

    cmd_parsers = parser.add_subparsers(help='command help')

    run_parser = cmd_parsers.add_parser('run', help='run a script.')
    run_parser.set_defaults(func=_run)

    script_parsers = run_parser.add_subparsers(help='script help')
    for script_name in scripts.all_scripts():
        script = scripts.get_script_by_name(script_name)
        script_parser = script_parsers.add_parser(script_name)
        script.add_argparse_args(script_parser)
        script_parser.set_defaults(script_cls=script)

    ns = parser.parse_args() if args is None else parser.parse_args(args)

    try:
        return ns.func(ns)
    except Exception as e:  # noqa
        if ns.show_stacktrace:
            raise e
        sys.stderr.write(str(e) + '\n'),
        sys.stderr.write('\trerun with qbc --show-stacktrace for more output\n')
        sys.stderr.write('\texample: qbc --show-stacktrace run blah\n')
        exit(1)


if __name__ == '__main__':
    main()
