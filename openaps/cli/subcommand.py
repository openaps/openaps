
class Subcommand (object):
  def __init__ (self, method=None):
    self.method = method
    self.name = method.__name__.split('.').pop( )

  def __repr__ (self):
    return ''.join(['<', self.__class__.__name__, ':', self.name ,'>'])

  def get_description (self):
    return ''.join(self.method.__doc__.split("\n\n")[0:1])

  def get_epilog (self):
    return ''.join(self.method.__doc__.split("\n\n")[1:])

  def configure_subparser (self, subparser):
    parser = subparser.add_parser(self.name, help=self.get_description( ), description=self.get_epilog( ))
    self.parser = parser
    return parser

  def _no_op_config (self, parser):
    pass

  def __call__ (self, args, app):
    self.method.main(args, app)

  def configure_parser (self, parser):
    getattr(self.method, 'configure_parser', self._no_op_config)(parser)
