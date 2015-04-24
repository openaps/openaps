
"""
Medtronic - openaps driver for Medtronic
"""
from openaps.uses.use import Use
import decocare

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


__USES__ = { }
def use ( ):
  def decorator (cls):
    if cls.__name__ not in __USES__:
      __USES__[cls.__name__] = cls
    return cls
  return decorator

@use( )
class scan (Use):
  """ scan for usb stick """
  def scanner (self):
    from decocare.scan import scan
    return scan( )
  def main (self, args, app):
    return self.scanner( )

class MedtronicTask (scan):
  requires_session = True
  record_stats = True
  def before_main (self, args, app):
    self.setup_medtronic( )
    pass
  def setup_medtronic (self):
    self.uart = stick.Stick(link.Link(self.scanner( )))
    self.uart.open( )
    serial = self.device.fields['serial']
    self.pump = session.Pump(self.uart, serial)
    stats = uart.interface_stats( )
  def main (self, args, app):
    return self.scanner( )
class Session (MedtronicTask):
  """ session for pump
  """
  def main (self, args, app):
    print "I'm medtronic %s command" % self.name
    print self.method, self.method.name, self.method.fields
    print args
    print app
    print app.config

@use( )
class Device (Session):
  """ Made up fae command
  """
  pass

@use( )
class Pump (Session):
  """ Query pump model
  """
  pass

@use( )
class CGM (Session):
  """ Query CGM model
  """
  pass

def set_config (args, device):
  device.add_option('serial', args.serial)

def display_device (device):
  return ''

known_uses = [
  Session,
  # Device, Pump, CGM
] + __USES__.values( )
def get_uses (device, config):
  return  known_uses[:]



