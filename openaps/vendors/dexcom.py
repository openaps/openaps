
"""
Dexcom - openaps driver for dexcom
"""
from openaps.uses.use import Use
from openaps.uses.registry import Registry
import dexcom_reader
from dexcom_reader import readdata
from datetime import datetime
import dateutil
from dateutil import relativedelta
from dateutil.parser import parse

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
class battery (scan):
  def main (self, args, app):
    battery = dict( level=self.dexcom.ReadBatteryLevel( )
                  , status=self.dexcom.ReadBatteryState( )
                  )
    return battery

@use( )
class ReadBatteryLevel (scan):
  def main (self, args, app):
    return self.dexcom.ReadBatteryLevel( )

@use( )
class ReadBatteryState (scan):
  def main (self, args, app):
    return self.dexcom.ReadBatteryState( )

@use( )
class ReadManufacturingData (scan):
  def main (self, args, app):
    data = self.dexcom.ReadManufacturingData( )
    result = data.attrib
    return result

@use( )
class GetFirmwareHeader (scan):
  def main (self, args, app):
    data = self.dexcom.GetFirmwareHeader( )
    result = data.attrib
    return result

@use( )
class ReadTransmitterId (scan):
  def main (self, args, app):
    result = self.dexcom.ReadTransmitterId( )
    return result

class SameNameCommand (scan):
  def pass_result (self, result):
    return result
  def main (self, args, app):
    name = self.__class__.__name__.split('.').pop( )
    result = getattr(self.dexcom, name)(**self.get_params(args))
    return self.pass_result(result)

@use( )
class ReadLanguage (SameNameCommand):
  """Read Language """


@use( )
class ReadRTC (SameNameCommand):
  """Read RTC """

@use( )
class ReadSystemTime (SameNameCommand):
  """Read System Time """

@use( )
class ReadSystemTimeOffset (SameNameCommand):
  """Read System Time Offset"""
  def pass_result (self, result):
    return result.total_seconds( )

@use( )
class ReadDisplayTime (SameNameCommand):
  """Read Display Time Offset"""

@use( )
class ReadDisplayTimeOffset (ReadSystemTimeOffset):
  """Read Display Time Offset"""

@use( )
class ReadGlucoseUnit (SameNameCommand):
  """Read Glucose Unit """

@use( )
class ReadClockMode (SameNameCommand):
  """Read Clock Mode """


@use( )
class ReadDeviceMode (SameNameCommand):
  """Read Device Mode """



@use( )
class glucose (scan):
  """ glucose

  This is a good example of what is needed for new commands.
  To add additional commands, subclass from scan as shown.
  """
  RECORD_TYPE = 'EGV_DATA'
  TEXT_COLUMNS = [ 'display_time', 'glucose', 'trend_arrow' ]
  def prerender_stdout (self, data):
    return self.prerender_text(data)
  def prerender_text (self, data):
    """ turn everything into a string """
    out = [ ]
    for item in data:
      line = map(str, [ item[field] for field in self.TEXT_COLUMNS ])
      out.append(' '.join(line))
    return "\n".join(out)
  def prerender_json (self, data):
    """ since everything is a dict/strings/ints, we can pass thru to json """
    return data
  def main (self, args, app):
    """
    Implement a main method that takes args and app as parameters.
    Use self.dexcom.Read... to get data.
    Return the resulting data for this task/command.
    The data will be passed to prerender_<format> by the reporting system.
    """
    # records = self.dexcom.ReadRecords('EGV_DATA')
    records = self.dexcom.ReadRecords(self.RECORD_TYPE)
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
  RECORD_TYPE = 'EGV_DATA'
  def get_params (self, args):
    return dict(count=int(args.count))
  def configure_app (self, app, parser):
    parser.add_argument('count', type=int, nargs='?', default=100,
                        help="Number of glucose records to read.")

  def main (self, args, app):
    records = [ ]
    for item in self.dexcom.iter_records(self.RECORD_TYPE):
      records.append(item.to_dict( ))
      # print len(records)
      if len(records) >= self.get_params(args)['count']:
        break
    return records


@use( )
class iter_glucose_hours (glucose):
  """ read last <hours> of glucose records, default 1, eg:

* iter_glucose_hours     - read last 1 hour of glucose records
* iter_glucose_hours 4.3 - read last 4.3 hours of glucose records
  """

  def get_params (self, args):
    return dict(hours=float(args.hours))
  
  def configure_app (self, app, parser):
    parser.add_argument('hours', type=float, nargs='?', default=1,
                        help="Number of hours of glucose records to read.")

  def main (self, args, app):
    params = self.get_params(args)
    delta = relativedelta.relativedelta(hours=params.get('hours'))
    now = datetime.now( )
    since = now - delta
    records = [ ]
    for item in self.dexcom.iter_records(self.RECORD_TYPE):
      if item.display_time >= since:
        records.append(item.to_dict( ))
      else:
        break
    return records


@use( )
class sensor (glucose):
  """Fetch Sensor (raw) records from Dexcom receiver.

  Fetches raw records.
  """
  RECORD_TYPE = 'SENSOR_DATA'
  TEXT_COLUMNS = [ 'display_time', 'unfiltered', 'filtered', 'rssi' ]

@use( )
class iter_sensor (iter_glucose, sensor):
  RECORD_TYPE = 'SENSOR_DATA'
  TEXT_COLUMNS = [ 'display_time', 'unfiltered', 'filtered', 'rssi' ]

@use( )
class iter_sensor_hours (iter_glucose_hours, iter_sensor):
  RECORD_TYPE = 'SENSOR_DATA'
  TEXT_COLUMNS = [ 'display_time', 'unfiltered', 'filtered', 'rssi' ]


@use( )
class meter_data (sensor):
  """
  Fetch METER_DATA records from the Dexcom receiver.
  """
  RECORD_TYPE = 'METER_DATA'
  TEXT_COLUMNS = [ 'display_time', 'system_time', 'meter_time', 'meter_glucose'  ]

@use( )
class iter_meter_data (iter_sensor, meter_data):
  RECORD_TYPE = 'METER_DATA'
  TEXT_COLUMNS = meter_data.TEXT_COLUMNS

@use( )
class iter_meter_data_hours (iter_sensor_hours, iter_meter_data):
  RECORD_TYPE = 'METER_DATA'
  TEXT_COLUMNS = meter_data.TEXT_COLUMNS


@use( )
class insertion_time (sensor):
  """
  Fetch INSERTION_TIME records from the Dexcom receiver.

  These are created when sensors are started.
  """
  RECORD_TYPE = 'INSERTION_TIME'
  TEXT_COLUMNS = [ 'display_time', 'system_time', 'insertion_time', 'session_state' ]

@use( )
class iter_insertion_time (iter_sensor, insertion_time):
  RECORD_TYPE = insertion_time.RECORD_TYPE
  TEXT_COLUMNS = insertion_time.TEXT_COLUMNS

@use( )
class iter_insertion_time_hours (iter_sensor_hours, iter_insertion_time):
  RECORD_TYPE = insertion_time.RECORD_TYPE
  TEXT_COLUMNS = insertion_time.TEXT_COLUMNS



@use( )
class user_event_data (sensor):
  """
  Fetch USER_EVENT_DATA records from the Dexcom receiver.
  """
  RECORD_TYPE = 'USER_EVENT_DATA'
  TEXT_COLUMNS = [ 'display_time', 'system_time', 'event_type', 'event_sub_type', 'event_value' ]


@use( )
class iter_user_event_data (iter_sensor, user_event_data):
  RECORD_TYPE = user_event_data.RECORD_TYPE
  TEXT_COLUMNS = user_event_data.TEXT_COLUMNS

@use( )
class iter_user_event_data_hours (iter_sensor_hours, iter_user_event_data):
  RECORD_TYPE = user_event_data.RECORD_TYPE
  TEXT_COLUMNS = user_event_data.TEXT_COLUMNS

@use( )
class sensor_insertions (scan):
  """ read sensor insertion, removal, and expiration records of sensors

  """
  def prerender_stdout (self, data):
    return self.prerender_text(data)
  def prerender_text (self, data):
    """ turn everything into a string """
    out = [ ]
    for item in data:
      line = map(str, [
        item['system_time']
      , item['insertion_time']
      , item['session_state']
      , item['display_time']
      ])
      out.append(' '.join(line))
    return "\n".join(out)
  def prerender_json (self, data):
    """ since everything is a dict/strings/ints, we can pass thru to json """
    return data
  def main (self, args, app):
    """
    Implement a main method that takes args and app as parameters.
    Use self.dexcom.Read... to get data.
    Return the resulting data for this task/command.
    The data will be passed to prerender_<format> by the reporting system.
    """
    records = self.dexcom.ReadRecords('INSERTION_TIME')
    # return list of dicts, easier for json
    out = [ ]
    for item in records:
      # turn everything into dict
      out.append(item.to_dict( ))
    return out

@use( )
class iter_sensor_insertions (sensor_insertions):
  """ read last <count> sensor insertion, removal, and expiration records, default 10, eg:

* iter_sensor_insertions   - read last 10 records
* iter_sensor_insertions 2 - read last 2 records
  """
  def get_params (self, args):
    return dict(count=int(args.count))
  def configure_app (self, app, parser):
    parser.add_argument('count', type=int, nargs='?', default=10,
                        help="Number of sensor insertion, removal, and expiration records to read.")

  def main (self, args, app):
    records = [ ]
    for item in self.dexcom.iter_records('INSERTION_TIME'):
      records.append(item.to_dict( ))
      # print len(records)
      if len(records) >= self.get_params(args)['count']:
        break
    return records

@use( )
class iter_sensor_insertions_hours (sensor_insertions):
  """ read last <hours> of sensor insertion, removal, and expiration records, default 1, eg:

* iter_sensor_insertions_hours     - read last 1 hour of sensor insertion, removal, and expiration records
* iter_sensor_insertions_hours 4.3 - read last 4.3 hours of sensor insertion, removal, and expiration records
  """

  def get_params (self, args):
    return dict(hours=float(args.hours))
  
  def configure_app (self, app, parser):
    parser.add_argument('hours', type=float, nargs='?', default=1,
                        help="Number of hours of sensor insertion, removal, and expiration records to read.")

  def main (self, args, app):
    params = self.get_params(args)
    delta = relativedelta.relativedelta(hours=params.get('hours'))
    now = datetime.now( )
    since = now - delta

    records = [ ]
    for item in self.dexcom.iter_records('INSERTION_TIME'):
      if item.system_time >= since:
        records.append(item.to_dict( ))
      else:
        break
    return records

@use( )
class calibrations (scan):
  """ read calibration entry records

  """
  def prerender_stdout (self, data):
    return self.prerender_text(data)
  def prerender_text (self, data):
    """ turn everything into a string """
    out = [ ]
    for item in data:
      line = map(str, [
        item['system_time']
      , item['meter_time']
      , item['display_time']
      , item['meter_glucose']
      ])
      out.append(' '.join(line))
    return "\n".join(out)
  def prerender_json (self, data):
    """ since everything is a dict/strings/ints, we can pass thru to json """
    return data
  def main (self, args, app):
    """
    Implement a main method that takes args and app as parameters.
    Use self.dexcom.Read... to get data.
    Return the resulting data for this task/command.
    The data will be passed to prerender_<format> by the reporting system.
    """
    records = self.dexcom.ReadRecords('METER_DATA')
    # return list of dicts, easier for json
    out = [ ]
    for item in records:
      # turn everything into dict
      out.append(item.to_dict( ))
    return out

@use( )
class iter_calibrations (calibrations):
  """ read last <count> calibration records, default 10, eg:

* iter_calibrations   - read last 10 calibration records
* iter_calibrations 2 - read last 2 calibration records
  """
  def get_params (self, args):
    return dict(count=int(args.count))
  def configure_app (self, app, parser):
    parser.add_argument('count', type=int, nargs='?', default=10,
                        help="Number of calibration records to read.")

  def main (self, args, app):
    records = [ ]
    for item in self.dexcom.iter_records('METER_DATA'):
      records.append(item.to_dict( ))
      # print len(records)
      if len(records) >= self.get_params(args)['count']:
        break
    return records

@use( )
class iter_calibrations_hours (calibrations):
  """ read last <hours> of calibration records, default 1, eg:

* iter_calibrations_hours     - read last 1 hour of calibration records
* iter_calibrations_hours 4.3 - read last 4.3 hours of calibration records
  """

  def get_params (self, args):
    return dict(hours=float(args.hours))
  
  def configure_app (self, app, parser):
    parser.add_argument('hours', type=float, nargs='?', default=1,
                        help="Number of hours of sensor insertion, removal, and expiration records to read.")

  def main (self, args, app):
    params = self.get_params(args)
    delta = relativedelta.relativedelta(hours=params.get('hours'))
    now = datetime.now( )
    since = now - delta

    records = [ ]
    for item in self.dexcom.iter_records('METER_DATA'):
      if item.system_time >= since:
        records.append(item.to_dict( ))
      else:
        break
    return records

