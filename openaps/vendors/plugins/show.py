
"""
Show/list vendor plugins

"""

from vendor import Vendor

def configure_app (app, parser):
  parser.set_defaults(name='*')
  parser._actions[-1].nargs = '?'
  parser._actions[-1].choices.append('*')

def main (args, app):
  for plugin in Vendor.FromConfig(app.config):
    if args.name in [ '*', plugin.name ]:
      print plugin.format_url( )

