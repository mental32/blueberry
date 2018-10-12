#!/usr/bin/python3

import sys

assert sys.version_info >= (3, 5), "fatal: required Python 3.5+"

if '.' not in sys.path:
    sys.path.append('.')

import argparse

from blueberry import Blueberry


def main(args):
    port = args.port

    if args.parent is None and not args.singlehost:
        sys.exit('blueberry: missing operand "parent"')

    if not args.singlehost:
        parent = args.parent
    else:
        parent = None

    app = Blueberry(parent, port)
    app.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('parent', metavar='parent', nargs='?')
    parser.add_argument('-p', dest='port', default='3722', type=int)
    parser.add_argument('--standalone', dest='singlehost', action='store_true')
    main(parser.parse_args())
