
"""
Medtronic - openaps driver for Medtronic
"""

def configure_add_app (app, parser):
  parser.add_argument('serial')

def configure_app (app, parser):
  if app.parent.name == 'add':
    print "CONFIG INNER", app, app.parent.name, app.name
def configure_parser (parser):
  pass
def main (args, app):
  print "MEDTRONIC", args, app
  print "app commands", app.selected.name

class Session (object):
  pass

class Device (object):
  pass

class Pump (Device):
  pass

class CGM (Device):
  pass

def set_config (args, device):
  device.add_option('serial', args.serial)

def display_device (device):
  return ''
