
"""
Medtronic - openaps driver for Medtronic
"""
from openaps.uses.use import Use
from openaps.uses.registry import Registry
from openaps.configurable import Configurable
import decocare
import argparse
import json
from decocare import stick, session, link, commands, history
from datetime import datetime
from dateutil import relativedelta
from dateutil.parser import parse

def configure_use_app (app, parser):
  pass
  # parser.add_argument('foobar', help="LOOK AT ME")

def configure_add_app (app, parser):
  parser.add_argument('serial')

def configure_app (app, parser):
  if app.parent.name == 'add':
    """
    print "CONFIG INNER", app, app.parent.name, app.name
    """
def configure_parser (parser):
  pass
def main (args, app):
  """
  print "MEDTRONIC", args, app
  print "app commands", app.selected.name
  """


use = Registry( )

@use( )
class scan (Use):
  """ scan for usb stick """
  def configure_app (self, app, parser):
    pass
    # print "hahaha"
  def scanner (self):
    from decocare.scan import scan
    return scan( )
  def main (self, args, app):
    return self.scanner( )

import logging
import logging.handlers
class MedtronicTask (scan):
  requires_session = True
  save_session = True
  record_stats = True

  def before_main (self, args, app):
    self.setup_medtronic( )
    if self.requires_session:
      self.check_session(app)
    else:
      self.pump.setModel(number=self.device.get('model', ''))

  def after_main (self, args, app):
    if self.save_session:
      self.device.store(app.config)
      app.config.save( )
    if self.uart:
      self.uart.close( )

  def get_session_info (self):
    expires = self.device.get('expires', None)
    now = datetime.now( )
    out = dict(device=self.device.name
      , vendor=__name__
      , used=now
      )
    if expires is None or parse(expires) < now:
      fields = self.create_session( )
      out.update(**self.update_session_info(fields))
    else:
      out['expires'] = parse(expires)
      out['model'] = self.get_model( )
    return out

  def update_session_info (self, fields):
    out = { }
    self.device.extra.add_option('expires', fields['expires'].isoformat( ))
    self.device.extra.add_option('model', fields['model'])
    out['expires'] = fields['expires']
    out['model'] = fields['model']
    return out

  def create_session (self):
    minutes = int(self.device.get('minutes', 3))
    now = datetime.now( )
    self.pump.power_control(minutes=minutes)
    model = self.get_model( )
    offset = relativedelta.relativedelta(minutes=minutes) + relativedelta.relativedelta(minutes=-1)
    out = dict(device=self.device.name
      , model=model
      , vendor=__name__
      , created_at=now
      , started=now
      , expires=now + offset
      )
    return out
  def check_session (self, app):
    self.session = self.get_session_info( )
    self.device.add_option('model', self.device.get('model', self.get_model( )))
  def get_model (self):
    model = self.pump.read_model( ).getData( )
    return model
  def setup_medtronic (self):
    log = logging.getLogger(decocare.__name__)
    print self.device
    level = getattr(logging, self.device.get('logLevel', 'WARN'))
    address = self.device.get('logAddress', '/dev/log')
    log.setLevel(level)
    for previous in log.handlers[:]:
      log.removeHandler(previous)
    log.addHandler(logging.handlers.SysLogHandler(address=address))
    self.uart = stick.Stick(link.Link(self.scanner( )))
    self.uart.open( )
    serial = self.device.get('serial')
    self.pump = session.Pump(self.uart, serial)
    stats = self.uart.interface_stats( )
  def main (self, args, app):
    return self.scanner( )

class Session (MedtronicTask):
  """ session for pump
  """
  requires_session = False
  def configure_parser (self, parser):
    parser.add_argument('--minutes', type=int, default='10')
  def setup_application (self):
    """
    """
  def main (self, args, app):
    info = self.create_session( )
    info.update(**self.update_session_info(info))
    return info

@use( )
class model (MedtronicTask):
  """ Get model number
  """
  def configure_app (self, app, parser):
    pass
  def main (self, args, app):
    model = self.pump.read_model( ).getData( )
    return model

@use( )
class read_status (MedtronicTask):
  """ Get pump status
  """
  def main (self, args, app):
    return self.pump.model.read_status( )

@use( )
class status (read_status):
  """ Get pump status (alias for read_status)
  """

@use( )
class reservoir (MedtronicTask):
  """ Get pump remaining insulin
  """
  def main (self, args, app):
    return self.pump.model.read_reservoir( )

@use( )
class settings (MedtronicTask):
  """ Get pump settings
  """
  def main (self, args, app):
    return self.pump.model.read_settings( )

@use( )
class mytest (MedtronicTask):
  """ Testing read_settings
  """
  requires_session = False
  def main (self, args, app):
    return self.pump.model.my_read_settings( )

@use( )
class read_clock (MedtronicTask):
  """ Read date/time of pump
  """
  def main (self, args, app):
    return self.pump.model.read_clock( )

class SameNameCommand (MedtronicTask):
  def main (self, args, app):
    name = self.__class__.__name__.split('.').pop( )
    return getattr(self.pump.model, name)(**self.get_params(args))

@use( )
class read_temp_basal (SameNameCommand):
  """ Read temporary basal rates. """

@use( )
class read_settings (SameNameCommand):
  """ Read settings. """

@use( )
class read_carb_ratios (SameNameCommand):
  """ Read carb_ratios. """

@use( )
class read_basal_profile_std (SameNameCommand):
  """ Read default basal profile. """

@use( )
class read_basal_profile_A (SameNameCommand):
  """ Read basal profile A. """

@use( )
class read_basal_profile_B (SameNameCommand):
  """ Read basal profile B. """

@use( )
class read_selected_basal_profile (SameNameCommand):
  """ Fetch the currently selected basal profile. """

@use( )
class read_current_glucose_pages (SameNameCommand):
  """ Read current glucose pages. """

@use( )
class read_current_history_pages (SameNameCommand):
  """ Read current history pages. """

@use( )
class suspend_pump (SameNameCommand):
  """ Suspend pumping. """
  def main (self, args, app):
    result = super(suspend_pump, self).main(args, app)
    result.update(enacted_at=datetime.now( ))
    return result

@use( )
class resume_pump (suspend_pump):
  """ resume pumping. """

@use( )
class read_battery_status (SameNameCommand):
  """ Check battery status. """

@use( )
class read_bg_targets (SameNameCommand):
  """ Read bg targets. """

@use( )
class read_insulin_sensitivies (SameNameCommand):
  """ Read insulin sensitivies. """


@use( )
class read_glucose_data (SameNameCommand):
  """ Read pump glucose page
  """
  def configure_app (self, app, parser):
    parser.add_argument('page', type=int, default=0)

  def get_params (self, args):
    return dict(page=int(args.page))

class InputProgramRequired (MedtronicTask):
  def upload_program (self, program):
    raise NotImplementedError( )
  def get_params (self, args):
    return dict(input=args.input)
  def configure_app (self, app, parser):
    parser.add_argument('input', default='-')
  def get_program (self, args):
    params = self.get_params(args)
    program = json.load(argparse.FileType('r')(params.get('input')))
    return program
  def main (self, args, app):
    program = self.get_program(args)
    results = self.upload_program(program)
    program.update(timestamp=datetime.now( ), **results)
    return program

@use( )
class set_temp_basal (InputProgramRequired):
  """ Set temporary basal rates.
  """
  def upload_program (self, program):
    return self.pump.model.set_temp_basal(**program)

@use( )
class bolus (InputProgramRequired):
  """ Send bolus.
  """
  def upload_program (self, program):
    return self.pump.model.bolus(**program)

@use( )
class filter_glucose_date (SameNameCommand):
  """ Search for glucose pages including begin and end dates (iso 8601).
  """
  def get_params (self, args):
    return dict(begin=args.begin, end=args.end)
  def configure_app (self, app, parser):
    parser.add_argument('begin', default='')
    parser.add_argument('end', default='')

@use( )
class filter_isig_date (filter_glucose_date):
  """ Search for isig pages including begin and end dates (iso 8601).
  """

@use( )
class read_history_data (MedtronicTask):
  """ Read pump history page
  """
  def get_params (self, args):
    return dict(page=int(args.page))
  def configure_app (self, app, parser):
    parser.add_argument('page', type=int, default=0)

  def main (self, args, app):
    history = self.pump.model.read_history_data(**self.get_params(args))
    return history


@use( )
class iter_glucose (MedtronicTask):
  """ Read latest 100 glucose records
  """
  def get_params (self, args):
    return dict(count=int(args.count))
  def configure_app (self, app, parser):
    parser.add_argument('count', type=int, default=99)
  def range (self):
    return self.pump.model.iter_glucose_pages( )
  maxCount = 99
  def main (self, args, app):
    self.maxCount = self.get_params(args).get('count', self.maxCount)
    num = 0
    records = [ ]
    for rec in self.range( ):
      records.append(rec)
      num = num + 1
      if num > self.maxCount:
        break
    return records

@use( )
class iter_pump (iter_glucose):
  """ Read latest 100 pump records
  """
  def range (self):
    return self.pump.model.iter_history_pages( )


@use ( )
class iter_glucose_hours (MedtronicTask):
  """ Read latest n hours of glucose data
  """
  def get_params (self, args):
    params = dict(hours=float(args.hours))

    if 'now' in args and args.now is not None:
      params.update(now=args.now)

    return params

  def configure_app (self, app, parser):
    parser.add_argument('hours', type=float, help='The number of hours of historical data to retrieve')
    parser.add_argument('--now', help='A read_clock report filename from which to offset the hours')

  def range (self):
    return self.pump.model.iter_glucose_pages( )

  def get_record_timestamp (self, record):
    return parse(record['date']) if 'date' in record else None

  def main (self, args, app):
    params = self.get_params(args)
    min_offset = relativedelta.relativedelta(hours=params['hours'])
    min_timestamp = parse(json.load(argparse.FileType('r')(params['now']))) - min_offset if 'now' in params else None

    records = [ ]
    for rec in self.range( ):
      timestamp = self.get_record_timestamp(rec)

      if timestamp is not None and min_timestamp is None:
        min_timestamp = timestamp - min_offset

      if timestamp is None or timestamp >= min_timestamp:
        records.append(rec)
      else:
        break
    return records


@use ( )
class iter_pump_hours (iter_glucose_hours):
  """ Read latest n hours of pump records
  """
  def range (self):
    return self.pump.model.iter_history_pages( )

  def get_record_timestamp (self, record):
    return parse(record['timestamp']) if 'timestamp' in record else None


def set_config (args, device):
  device.add_option('serial', args.serial)

def display_device (device):
  return ''

known_uses = [
  Session,
]
def get_uses (device, config):
  all_uses = known_uses[:] + use.get_uses(device, config)
  all_uses.sort(key=lambda usage: getattr(usage, 'sortOrder', usage.__name__))
  return all_uses



