
import dexcom, medtronic

from openaps.cli.subcommand import Subcommand
from openaps.cli.commandmapapp import CommandMapApp

class ChangeVendorApp (Subcommand):

  def setup_application (self):
    name = 'configure_%s_app' % self.parent.name
    getattr(self.method, 'configure_app', self._no_op_setup)(self, self.parser)
    getattr(self.method, name, self._no_op_setup)(self, self.parser)

def find_plugins ( ):
  return [ ]

def get_vendors ( ):
  return [ dexcom, medtronic ]

def get_map ( ):
  vendors = all_vendors( )
  names = [ v.__name__.split('.').pop( ) for v in vendors ]
  return dict(zip(names, vendors))

def lookup (name):
  return get_map( )[name]

def all_vendors ( ):
  return get_vendors( ) + find_plugins( )
 
class VendorConfigurations (CommandMapApp):
  Subcommand = ChangeVendorApp
  def get_dest (self):
    return 'vendor'
  def get_commands (self):
    return all_vendors( )

  def get_vendor (self, vendor):
    return self.commands[vendor]
def get_configurable_devices (ctx):
  vendors = VendorConfigurations(ctx)
  return vendors

