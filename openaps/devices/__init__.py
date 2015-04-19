

import add, remove, show

from openaps.cli.subcommand import Subcommand
def configure_app (app, parser):
  print "CONFIG", app.config
  pass

class DeviceConfig (Subcommand):
  def setup_application (self):
    self.parser.add_argument('name')
    getattr(self.method, 'configure_app', self._no_op_setup)(self, self.parser)
def configure_commands (parser):
    subparsers = parser.add_subparsers(help="Operation", dest='command')
    commands = { }

    for ctx in [ add, remove, show ]:
      app = DeviceConfig(ctx)
      parser = app.configure_subparser(subparsers)
      app.configure_parser(parser)
      commands[app.name] = app

    return commands


