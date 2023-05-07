from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser(description='Messenger CLI')
    subparsers = parser.add_subparsers(dest='subparser_name')

    subparser = subparsers.add_parser("set")
    subparser.add_argument("set_key", metavar='key')
    subparser.add_argument("set_value", metavar='value')

    subparser = subparsers.add_parser("get")
    subparser.add_argument("get_key", metavar='key')

    subparser = subparsers.add_parser("send")
    subparser.add_argument("send_text", metavar='text', nargs='+')
    subparser.add_argument("--chat", required=True)

    return parser
