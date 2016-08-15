"""Keysmith Default Interface"""

import argparse
import math
import string
import sys

import keysmith


POPULATIONS = {
    'alphanumeric': string.ascii_letters + string.digits,
    'ascii_letters': string.ascii_letters,
    'digits': string.digits,
    'printable': string.printable,
}


def cli(parser=None):
    """Parse CLI arguments and options."""
    if parser is None:
        parser = argparse.ArgumentParser(
            prog=keysmith.CONSOLE_SCRIPT,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument(
        '-d', '--delimiter',
        help='a delimiter for the samples (teeth) in the key',
        default=' ',
    )
    parser.add_argument(
        '-n', '--nsamples',
        help='the number of random samples to take',
        type=int,
        default=3,
        dest='nteeth',
    )
    parser.add_argument(
        '-p', '--population',
        help=', '.join(POPULATIONS.keys()) + ', or a path to a file of line-delimited items',
        default='/usr/share/dict/words',
    )
    parser.add_argument(
        '--encoding',
        help='the encoding of the population file'
             ' (see https://docs.python.org/3/library/codecs.html#standard-encodings)',
        default='utf-8',
    )
    parser.add_argument(
        '--stats',
        help='show statistics for the key',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {0}'.format(keysmith.__version__),
    )
    return parser


def main(args=None):
    """Execute CLI commands."""

    if args is None:
        args = cli().parse_args()

    seq = POPULATIONS.get(args.population)
    if seq is None:
        try:
            with open(args.population, 'r', encoding=args.encoding) as f:
                seq = list(f)
        except (OSError, UnicodeError) as ex:
            print(ex, file=sys.stderr)
            return 1

    key = keysmith.key(seq=seq, nteeth=args.nteeth, delimiter=args.delimiter)
    print(key)

    if args.stats:
        print('* {0} characters'.format(len(key)))
        print('* {0} samples from a population of {1}'.format(args.nteeth, len(seq)))
        print('* entropy {sign} {bits} bits'.format(
            sign='<' if len(args.delimiter) < 1 else '~',
            bits=round(math.log(len(seq), 2) * args.nteeth, 2),
        ))

    return 0


if __name__ == '__main__':
    sys.exit(main())
