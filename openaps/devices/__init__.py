

import add, remove, show

from openaps.cli.subcommand import Subcommand

def configure_commands (parser):
    subparsers = parser.add_subparsers(help="Operation", dest='command')
    commands = { }

    for ctx in [ add, remove, show ]:
      app = Subcommand(ctx)
      parser = app.configure_subparser(subparsers)
      app.configure_parser(parser)
      commands[app.name] = app

    return commands


