import sys
class Device (object):
  name = None
  vendor = None
  required = ['name', 'vendor']
  optional = [ ]
  prefix = 'device'

  # optional = [ 'serial' ]
  def __init__ (self, name, config):
    self.name = name
    self._config = config 
  def section_name (self):
    return '%s "%s"' % (self.prefix, self.name)
  def add_option (self, k, v):
    section = self.section_name( )
    self._config.set(section, k, v)
    if k not in self.required + self.optional:
      self.optional.append(k)
  def configure (self, config):
    section = self.section_name( )
    for opt in self.required + self.optional:
      config.set(section, opt, getattr(self, opt))

class Config (object):
  config = None
  def __init__ (self, config, item):
    self.config = config
    self.item = item

  def get (self):
    items = [ ]
    for name in self.config.sections( ):
      attrs = { }
      if name.startswith(self.item.prefix):
        items.push(name)
    return items 

  def lint (self):
    return True

