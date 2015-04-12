
import sys, os
import argparse
import argcomplete

class Base (object):
  
  def __init__ (self, args):
    self.inputs = args

  def prep_parser (self):
    self.parser = argparse.ArgumentParser( )

  def configure_parser (self, parser):
    pass

  def __call__ (self):
    self.prep_parser( )
    self.configure_parser(self.parser)
    argcomplete.autocomplete(self.parser);
    self.args = self.parser.parse_args( )
    self.run(self.args)

  def run (self, args):
    print self.inputs
    print args

