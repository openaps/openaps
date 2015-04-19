
import sys, os
import argparse
import argcomplete
import textwrap

class Base (object):
  
  always_complete_options = True
  def __init__ (self, args):
    self.inputs = args

  @classmethod
  def _get_description (klass):
    return klass.__doc__.split("\n\n")[0]

  @classmethod
  def _get_epilog (klass):
    return "\n\n".join(klass.__doc__.split("\n\n")[1:])

  def prep_parser (self):
    epilog = textwrap.dedent(self._get_epilog( ))
    description = self._get_description( )
    self.parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

  def configure_parser (self, parser):
    pass

  def prolog (self):
    pass

  def epilog (self):
    pass

  def __call__ (self):
    self.prep_parser( )
    self.configure_parser(self.parser)
    argcomplete.autocomplete(self.parser, always_complete_options=self.always_complete_options);
    self.args = self.parser.parse_args( )
    self.prolog( )
    self.run(self.args)
    self.epilog( )

  def run (self, args):
    print self.inputs
    print args

