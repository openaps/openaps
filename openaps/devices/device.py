import json
from openaps.configurable import Configurable
class Device (Configurable):
  vendor = None
  required = ['name', 'vendor']
  optional = [ ]
  prefix = 'device'
  _uses = [ ]

  def __init__ (self, name, vendor):
    self.name = name
    self.vendor = vendor
    self.fields = dict(vendor=vendor.__name__)

  def read (self, args=None, config=None):
    if args:
      self.vendor.set_config(args, self)
      self.name = args.name
    if config:
      # self.vendor.read_config(config)
      self.fields.update(dict(config.items(self.section_name( ))))

  def format_url (self):
    parts = ['{0:s}://{1:s}'.format(self.vendor.__name__.split('.').pop( ), self.name), ]
    parts.append(self.vendor.display_device(self))
    return ''.join(parts)

  def register_uses (self, uses):
    for u in uses.usages:
      if u not in self._uses:
        self._uses.append(u)

  @classmethod
  def FromConfig (klass, vendors, config):
    devices = [ ]
    for candidate in config.sections( ):
      if candidate.startswith(klass.prefix):
        name = json.loads(candidate.split(' ').pop( ))
        vendor = vendors.lookup(config.get(candidate, 'vendor').split('.').pop( ), config)
        device = klass(name, vendor)
        device.read(config=config)
        devices.append(device)
    return devices

