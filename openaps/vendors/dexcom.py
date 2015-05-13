
"""
Dexcom - openaps driver for dexcom
"""
from openaps.uses.use import Use
from openaps.uses.registry import Registry
import dexcom_reader
from dexcom_reader import readdata

def set_config (args, device):
  return

def display_device (device):
  return ''

use = Registry( )

get_uses = use.get_uses

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
  """ glucose

  This is a good example of what is needed for new commands.
  To add additional commands, subclass from scan as shown.
  """
  def prerender_stdout (self, data):
    return self.prerender_text(data)
  def prerender_text (self, data):
    """ turn everything into a string """
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
    """ since everything is a dict/strings/ints, we can pass thru to json """
    return data
  def main (self, args, app):
    """
    Implement a main method that takes args and app as parameters.
    Use self.dexcom.Read... to get data.
    Return the resulting data for this task/command.
    The data will be passed to prerender_<format> by the reporting system.
    """
    records = self.dexcom.ReadRecords('EGV_DATA')
    # return list of dicts, easier for json
    out = [ ]
    for item in records:
      # turn everything into dict
      out.append(item.to_dict( ))
    return out

@use( )
class iter_glucose (glucose):
  """ read last <count> glucose records, default 100, eg:

* iter_glucose   - read last 100 records
* iter_glucose 2 - read last 2 records
  """
  def get_params (self, args):
    return dict(count=int(args.count))
  def configure_app (self, app, parser):
    parser.add_argument('count', type=int, nargs='?', default=100,
                        help="Number of glucose records to read.")

  def main (self, args, app):
    records = [ ]
    for item in self.dexcom.iter_records('EGV_DATA'):
      records.append(item.to_dict( ))
      # print len(records)
      if len(records) >= self.get_params(args)['count']:
        break
    return records

