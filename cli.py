#!/bin/env python
import argparse
from jinja2 import Environment, DictLoader, select_autoescape

structure = '''
#!/bin/env python

import argparse
import logging

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='{{ description }}')
{% for arg in args %}
  {% if not arg.required %}__DEBUG_1__
    {% if arg.dest is defined and arg.dest|length %}__DEBUG_2__
    parser.add_argument('{{ arg.short }}', '{{ arg.long }}', dest={{ arg.dest }},
                        default={{ arg.default }}, help='{{ arg.help_str }}')
    {% else %}__DEBUG_3__
    parser.add_argument('{{ arg.short }}', '{{ arg.long }}', default={{ arg.default }},
                        help='{{ arg.help_str }}')
    {% endif %}__DEBUG_2__
  {% else %}__DEBUG_4__
    {% if arg.dest is defined and arg.dest|length %}__DEBUG_5__
    parser.add_argument('{{ arg.short }}', '{{ arg.long }}', dest={{ arg.dest }},
                        required=True, default={{ arg.default }}, help='{{ arg.help_str }}')
    {% else %}__DEBUG_6__
    parser.add_argument('{{ arg.short }}', '{{ arg.long }}', default={{ arg.default }},
                        required=True, help='{{ arg.help_str }}')
    {% endif %}__DEBUG_5__
  {% endif %}__DEBUG_4__
{% endfor %}
    args = parser.parse_args()

    # Do Stuff

if __name__ == '__main__':
    main()
'''
structure2 = '''
{% for arg in args %}
short = {{ arg.short }}
long = {{ arg.long }}
default = {{ arg.default }}
help_str = {{ arg.help_str }}
required = {{ arg.required }}
dest = {{ arg.dest }}
{% endfor %}
'''
env = Environment(loader=DictLoader({'source': structure}))


def main():
    parser = argparse.ArgumentParser(description='Run dataspec.')
    parser.add_argument('-a', '--args', nargs='+',
        help="One or more args to add, format: 'name:default:helpstr:required', last three parts are optional")

    args = parser.parse_args()

    variables = populate_template_vars(args)
    template = env.get_template('source')
    lines = template.render(variables).split('\n')
    for line in lines:
        if '__DEBUG_' in line:
            continue
        print(line)


def populate_template_vars(args):
    data = []
    # Do Stuff
    for arg in args.args:
        parts = arg.split(':')
        name = parts[0]
        short = f'-{name[0]}'
        long = f'--{name}'

        default = get_part_or_default(parts, 1, '')
        if not default.isnumeric():
            default = f'"{default}"'

        help_str = get_part_or_default(parts, 2, f'TODO: Fill in help for {name}')
        required = get_part_or_default(parts, 3, False)
        if str(required).lower() in ['t', 'true']:
            required = True
        else:
            required = False
        if '-' in name:
            dest = name.replace('-', '_')
        else:
            dest = ''
        data.append(TemplateVar(short, long, default, help_str, required, dest))
    return {'args': data}


def get_part_or_default(parts, idx, default):
    if len(parts) > idx:
        return parts[idx]
    return default


class TemplateVar:
    def __init__(self, short, long, default, help_str, required, dest):
        self.short = short
        self.long = long
        self.default = default
        self.help_str = help_str
        self.required = required
        self.dest = dest


if __name__ == '__main__':
    main()
