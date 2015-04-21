

from openaps.cli.subcommand import Subcommand
class Use (Subcommand):
  """A no-op base use."""
  pass
  def __init__ (self, method=None, parent=None):
    self.method = method
    self.name = self.__class__.__name__.split('.').pop( )
    self.parent = parent
  def main (self, args, app):
    print "HAHA", args, app

