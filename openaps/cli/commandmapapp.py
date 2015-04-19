
from subcommand import Subcommand

class CommandMapApp (object):

  Subcommand = Subcommand
  commands = { }
  def __init__ (self, parent):
    self.parent = parent
    self.commands = { }

  def get_help (self):
    return "Operation"
  def get_dest (self):
    return 'command'

  def get_commands (self):
    return [ ]
    
  def configure_commands (self, parser):
      subparsers = parser.add_subparsers(help=self.get_help( ), dest=self.get_dest( ))
      self.subparsers = subparsers

      for ctx in self.get_commands( ):
        self.makeSubcommand(ctx)

      return self.commands

  def selected (self, args):
    selected = getattr(args, self.get_dest( ))
    return self.commands[selected]
  def get (self, name):
    return self.commands[name]
  def makeSubcommand (self, ctx):
      app = self.Subcommand(ctx, parent=self.parent)
      parser = app.configure_subparser(self.subparsers)
      app.configure_parser(parser)
      self.commands[app.name] = app
