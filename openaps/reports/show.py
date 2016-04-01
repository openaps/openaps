
"""
show   - show all reports
"""

from openaps.devices.device import Device
from openaps.reports.report import Report

from openaps.cli import helpers

class Formatter (object):
  def __init__ (self, app):
    self.app = app
  def __call__ (self, thing):
    return self.format_cli(thing)

  def format_cli (self, report):
    usage = self.app.devices[report.fields.get('device')]
    task = self.app.actions.commands['add'].usages.commands[usage.name].method.commands[report.fields['use']]

    line = [ 'openaps', 'use', usage.name, report.fields.get('use') ]
    params = [ ]
    for param in usage.extra.fields.get('fields', '').split(' '):
      params.append(report.fields.get(param, ''))
    params.append(report.fields.get('remainder', ''))
    return ' '.join(line + params)
def configure_app (app, parser):
  parser.set_defaults(report='*')
  parser._actions[-1].nargs = '?'
  if parser._actions[-1].choices:
    parser._actions[-1].choices.append('*')
  helpers.install_show_arguments(parser)
  parser.add_argument('--cli_only', action='store_const', default=False, const=True)

def main (args, app):
  format_cli = Formatter(app)
  for device in Report.FromConfig(app.config):
    if args.report in [ '*', device.name ]:
      if args.cli_only:
        print format_cli(device)
      else:
        print args.format(device)

