import json
class Report (object):
  prefix = 'report'
  required = [ 'reporter', 'report', 'device', 'use' ]
  optional = [ ]
  fields = { }
  name = None
  def __init__ (self, report=None, reporter=None, device=None, use=None):
    self.name = report
    self.fields = dict(reporter=reporter, device=device, use=use)

  def format_url (self):
    template = "{device:s}://{reporter:s}/{use:s}/{report:s}"
    return template.format(report=self.name, **self.fields)

  def section_name (self):
    return '%s "%s"' % (self.prefix, self.name)

  def add_option (self, k, v):
    self.fields[k] = v
    if k not in self.required + self.optional:
      self.optional.append(k)

  def items (self):
    return self.fields.items( )

  def store  (self, config):
    config.add_device(self)

  def remove (self, config):
    config.remove_device(self)

  @classmethod
  def FromConfig (klass, config):
    reports = [ ]
    for candidate in config.sections( ):
      if candidate.startswith(klass.prefix):
        name = json.loads(candidate.split(' ').pop( ))
        # for f in klass.required:
        fields = dict(config.items(candidate))
        report = klass(report=name, **fields)
        reports.append(report)
    return reports
