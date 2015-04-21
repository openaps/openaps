
"""
Medtronic - openaps driver for Medtronic
"""
from openaps.uses.use import Use

def configure_use_app (app, parser):
  pass
  # parser.add_argument('foobar', help="LOOK AT ME")

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

class Session (Use):
  """ session for pump
  """
  def main (self, args, app):
    print "I'm medtronic session command"
    print self.method, self.method.name, self.method.fields
    print args
    print app
    print app.config

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

known_uses = [
  Session
]
def get_uses (device, config):
  return  known_uses[:]



