
"""
show   - show all aliases
"""

from alias import Alias

def configure_app (app, parser):
  parser.set_defaults(name='*')
  parser._actions[-1].nargs = '?'
  if parser._actions[-1].choices:
    parser._actions[-1].choices.append('*')

def main (args, app):
  for device in Alias.FromConfig(app.config):
    if args.name in [ '*', device.name ]:
      print device.format_url( )

