
"""
Dexcom - openaps driver for dexcom
"""
from openaps.uses.use import Use
import dexcom_reader
from dexcom_reader import readdata

def set_config (args, device):
  return

def display_device (device):
  return ''

__USES__ = { }
def use ( ):
  def decorator (cls):
    if cls.__name__ not in __USES__:
      __USES__[cls.__name__] = cls
    return cls
  return decorator

known_uses = [ ]
def get_uses (device, config):
  return  known_uses[:] + __USES__.values( )

@use( )
class scan (Use):
  """ scan for usb stick """
  def scanner (self):
    return readdata.Dexcom.FindDevice( )
  def main (self, args, app):
    return self.scanner( ) or ''

