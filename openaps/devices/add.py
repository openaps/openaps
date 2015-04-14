
"""
add    - add a new device configuration
"""
from openaps import vendors

def configure_app (app, parser):
  commands = vendors.get_configurable_devices(app)
  app.vendors = commands
  commands.configure_commands(parser)

def configure_parser (parser):
  pass

def main (args, app):
  print "adding", app.selected.vendors.selected(args)
  print app.selected.vendors.selected(args)(args, app)

