

from openaps.cli.subcommand import Subcommand
class Use (Subcommand):
  """A no-op base use."""
  pass
  def __init__ (self, method=None, parent=None):
    self.method = method
    self.name = self.__class__.__name__.split('.').pop( )
    self.parent = parent
    self.device = parent.device
  def main (self, args, app):
    """
    Put main app logic here.
    print "HAHA", args, app
    """

  def get_params (self, args):
    return dict( )
  def before_main (self, args, app):
    pass
  def after_main (self, args, app):
    pass
  def __call__ (self, args, app):
    self.before_main(args, app)
    output = self.main(args, app)
    self.after_main(args, app)
    return output
