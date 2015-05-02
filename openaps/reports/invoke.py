
"""
invoke   - generate a report
"""

from openaps.reports.report import Report
from openaps import uses
import reporters

def selected_usage (usages, key):
  for use in usages:
    name = use.__name__.split('.').pop( )
    if key == name:
      return use
def configure_app (app, parser):
  parser.set_defaults(report='*')
  parser._actions[-1].nargs = '?'
  if parser._actions[-1].choices:
    parser._actions[-1].choices.append('*')
  # print 'app', app.reports
def main (args, app):
  # reports = reporters.get_reporters( )
  report =  app.actions.selected(args).reports[args.report]
  device = app.devices[report.fields['device']]
  # available = uses.get_uses_for(device, app)
  # usage = selected_usage(available, report.fields['use'])
  # print usage
  task = app.actions.commands['add'].usages.commands[device.name].method.commands[report.fields['use']]
  # print task.name, task.usage, task.method
  # print device.name, device
  # print report.name, report.fields
  # XXX.bewest: very crude, need to prime the Use's args from the config
  for k, v in report.fields.items( ):
    setattr(args, k, v)
  # print args
  print report.format_url( )
  repo = app.git_repo( )
  reporter = reporters.Reporter(report, device, task)
  # print report.fields
  reporter(task.method(args, app))
  print 'reporting', report.name
  repo.index.add([report.name])

