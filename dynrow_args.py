# command-line arguments for DynRow

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default="You", help="use NAME for user boat name")  # --name <name on user boat>
    parser.add_argument('--loglevel', default="ERROR", help="logging level. One of: ERROR, WARNING, INFO, DEBUG")  
    parser.add_argument('--pyerg', help="use pyerg to access the erg instead of PyRow", action='store_true')
    return parser.parse_args()


# name = player's name (always present)
# pyerg True if flag passed, False if not
args = parse_args()
