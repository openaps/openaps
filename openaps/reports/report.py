import json
from openaps.configurable import Configurable
class Report (Configurable):
  prefix = 'report'
  required = [ 'reporter', 'report', 'device', 'use' ]
  optional = [ ]
  fields = { }
  url_template = "{device:s}://{reporter:s}/{use:s}/{name:s}"
  name = None
  def __init__ (self, report=None, reporter=None, device=None, use=None, **kwds):
    self.name = report
    self.fields = dict(reporter=reporter, device=device, use=use, **kwds)

