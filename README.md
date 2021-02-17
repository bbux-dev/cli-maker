CLI Maker - for creating a python cli tool quickly from a template
================================

This is a utility for generate an argparse based commandline program quickly.  It doesn't support
all of the argparse formats, but should be sufficient to generate the skeleton quickly. The format
is to specify a list of quoted strings that describe the `name:default:help:required` parameters for
the args that should be a part of the command line tool.  for `required` t or true signifies the param
is required. See example below.

```shell
./cli.py -a 'input::where to get the input:t' \
            'output:.:where to put the output' \
            'log-level:logging.INFO' \
            'num-iterations'

#!/bin/env python

import argparse
import logging

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--input', default="",
                        required=True, help='where to get the input')

    parser.add_argument('-o', '--output', default=".",
                        help='where to put the output')

    parser.add_argument('-l', '--log-level', dest=log_level,
                        default="logging.INFO", help='TODO: Fill in help for log-level')

    parser.add_argument('-n', '--num-iterations', dest=num_iterations,
                        default="", help='TODO: Fill in help for num-iterations')

    args = parser.parse_args()

    # Do Stuff

if __name__ == '__main__':
    main()
```
