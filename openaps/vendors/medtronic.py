
"""
Medtronic - openaps driver for Medtronic
"""


def configure_parser (parser):
  pass
def main (args, app):
  print "MEDTRONIC", __file__, args, app

class Config (object):
  config = None
  def __init__ (self, config):
    self.config = config

  def get (self, find=None):
    devices = [ ]
    for name in self.config.sections( ):
      attrs = { }
      if name.startswith('device "medtronic"'):
        devices.push(name)
    return devices

  def lint (self):
    return True

class Session (object):
  pass

class Device (object):
  pass

class Pump (Device):
  pass

class CGM (Device):
  pass

