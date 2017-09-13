
"""
Remove vendor plugin from openaps-environment
"""
from __future__ import print_function
from __future__ import absolute_import

from .vendor import Vendor
def main (args, app):
  for plugin in Vendor.FromConfig(app.config):
    if args.name == plugin.name:
      plugin.remove(app.config)
      app.config.save( )
      print('removed', plugin.format_url( ))
      break

