
"""
remove - remove a  device configuration
"""
from __future__ import print_function
from __future__ import absolute_import
from .report import Report
import sys
def main (args, app):
  for report in Report.FromConfig(app.config):
    if args.report == report.name:
      report.remove(app.config)
      app.config.save( )
      print('removed', report.format_url( ))
      break

