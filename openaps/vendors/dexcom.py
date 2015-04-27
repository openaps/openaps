
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
  def before_main (self, args, app):
    self.port = self.scanner( )
    self.dexcom = self.port and readdata.Dexcom(self.port) or None
  def main (self, args, app):
    return self.port or ''

@use( )
class glucose (scan):
  """  glucose """
  def prerender_text (self, data):
    out = [ ]
    for item in data:
      line = map(str, [
        item['display_time']
      , item['glucose']
      , item['trend_arrow']
      ])
      out.append(' '.join(line))
    return "\n".join(out)
  def prerender_JSON (self, data):
    return data
  def main (self, args, app):
    records = self.dexcom.ReadRecords('EGV_DATA')
    out = [ ]
    for item in records:
      out.append(item.to_dict( ))
    return out
