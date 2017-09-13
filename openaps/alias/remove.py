
"""
remove - remove an alias
"""
from __future__ import print_function
from __future__ import absolute_import
from .alias import Alias
def main (args, app):
  for alias in Alias.FromConfig(app.config):
    if args.name == alias.name:
      alias.remove(app.config)
      app.config.save( )
      print('removed', alias.format_url( ))
      break

