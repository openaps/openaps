
import dexcom, medtronic

from openaps.cli.subcommand import Subcommand
from openaps.cli.commandmapapp import CommandMapApp

from openaps.configurable import Configurable
class Vendor (Configurable):
  prefix = 'vendor'
  required = [ 'name', ]
  optional = [ ]
  fields = { }
  url_template = "{name:s}://"
  name = None
  def __init__ (self, name=None, **kwds):
    self.name = name
    self.fields = dict(**kwds)

  def get_module (self):
    import imp
    import importlib
    import site
    print 'XX', self.name, self.fields
    site.addsitedir(self.fields.get('path'))
    return importlib.import_module(self.name)
    fp, pathname, description = imp.find_module(self.name)
    try:
      module = imp.load_module(self.name, fp, pathname, description)
      return module
    finally:
      if fp:
        fp.close( )

class ChangeVendorApp (Subcommand):
  """
  Allow subcommand to handle setup_application
  """

def find_plugins (config):
  vendors = Vendor.FromConfig(config)
  for v in vendors:
    print v, v.name, v.fields
  print vendors
  return [ v.get_module( ) for v in vendors ]

def get_vendors ( ):
  return [ dexcom, medtronic ]

def get_map (config=None):
  vendors = all_vendors(config)
  names = [ v.__name__.split('.').pop( ) for v in vendors ]
  return dict(zip(names, vendors))

def lookup (name, config=None):
  return get_map(config)[name]

def all_vendors (config=None):
  return get_vendors( ) + find_plugins(config)
 
class VendorConfigurations (CommandMapApp):
  Subcommand = ChangeVendorApp
  def get_dest (self):
    return 'vendor'
  def get_commands (self):
    return all_vendors(self.parent.config)

  def get_vendor (self, vendor):
    return self.commands[vendor]

def get_configurable_devices (ctx):
  vendors = VendorConfigurations(ctx)
  return vendors

