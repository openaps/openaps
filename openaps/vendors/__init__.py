
import dexcom, medtronic

from openaps.cli.subcommand import Subcommand
from openaps.cli.commandmapapp import CommandMapApp

class ChangeVendorApp (Subcommand):

  pass

def find_plugins ( ):
  return [ ]

def get_vendors ( ):
  return [ dexcom, medtronic ]

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

