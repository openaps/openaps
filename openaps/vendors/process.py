"""
process - a fake vendor to run arbitrary commands
"""

import sys, os
import shlex
from subprocess import check_output, call

import argparse
from plugins.vendor import Vendor
from openaps.uses.use import Use
from openaps.uses.registry import Registry

use = Registry( )

def configure_add_app (app, parser):
  parser.add_argument('cmd')
  parser.add_argument('--require', action='append', default=[])
  parser.add_argument('args', nargs=argparse.REMAINDER)
  # .completer = complete_args

def configure_use_app (app, parser):
  print "HEY"
def configure_app (app, parser):
  print "HEY"
  pass

def main (args, app):
  print "dkljsdkljHEY"
  print "HEY"


def set_config (args, device):
  device.add_option('cmd', args.cmd)
  device.add_option('args', ' '.join(args.args))
  device.add_option('fields', ' '.join(args.require))

def display_device (device):
  return ''

@use( )
class shell (Use):
  """ run a process in a subshell
  """
  def get_params (self, args):
    self.fields = self.device.fields.get('fields').split(' ')
    params = dict( )
    for opt in self.fields:
      params[opt] = getattr(args, opt)
    return params

  def configure_app (self, app, parser):
    self.fields = self.device.fields.get('fields').split(' ')
    for opt in self.fields:
      parser.add_argument(opt)
  def main (self, args, app):
    info = self.device.fields
    command = [ info.get('cmd')
              ] + info.get('args').split(' ')
    for opt in self.fields:
      command.append(getattr(args, opt))
    command = shlex.split(' '.join(command))
    output = check_output(command)
    return output


known_uses = [
]

def get_uses (device, config):
  all_uses = known_uses[:] + use.__USES__.values( )
  all_uses.sort(key=lambda usage: getattr(usage, 'sortOrder', usage.__name__))
  return all_uses

