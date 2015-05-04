
"""
show   - show all devices
"""

from openaps.devices.device import Device
from openaps import vendors

def configure_app (app, parser):
  parser.set_defaults(name='*')
  parser._actions[-1].nargs = '?'
  parser._actions[-1].choices.append('*')
def main (args, app):
  # print args
  for device in Device.FromConfig(vendors, app.config):
    if args.name in [ '*', device.name ]:
      print device.format_url( )

