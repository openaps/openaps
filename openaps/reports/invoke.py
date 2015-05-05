
"""
invoke   - generate a report
"""

from openaps.reports.report import Report
from openaps import uses
import reporters

def configure_app (app, parser):
  """
  """

def main (args, app):
  report =  app.actions.selected(args).reports[args.report]
  device = app.devices[report.fields['device']]
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
  reporter(task.method(args, app))
  print 'reporting', report.name
  repo.index.add([report.name])

