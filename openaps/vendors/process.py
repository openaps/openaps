"""
process - a fake vendor to run arbitrary commands
"""

import sys, os
import shlex
from subprocess import check_output, call, PIPE
import subprocess

import argparse
from plugins.vendor import Vendor
from openaps.uses.use import Use
from openaps.uses.registry import Registry

# create a usage registry/decorator
use = Registry( )
# custom registry, to track usages
get_uses = use.get_uses

def configure_add_app (app, parser):
  parser.add_argument('cmd')
  parser.add_argument('--require', action='append', default=[])
  parser.add_argument('args', nargs=argparse.REMAINDER)
  # .completer = complete_args

def set_config (args, device):
  device.add_option('cmd', args.cmd)
  device.add_option('args', ' '.join(args.args))
  device.add_option('fields', ' '.join(args.require))

def display_device (device):
  data = dict(**device.fields)
  data.update(**device.extra.fields)
  return '/{cmd:s}/{args:s}'.format(**data)

@use( )
class shell (Use):
  """ run a process in a subshell
  """
  def get_params (self, args):
    self.fields = self.device.get('fields').strip( ).split(' ')
    params = dict(remainder=args.remainder)
    for opt in self.fields:
      if opt:
        params[opt] = getattr(args, opt)
    return params

  def configure_app (self, app, parser):
    self.fields = self.device.get('fields').strip( ).split(' ')
    for opt in self.fields:
      if opt:
        parser.add_argument(opt)
    parser.add_argument('remainder', nargs=argparse.REMAINDER)
  def main (self, args, app):
    # info = self.device.fields
    info = dict(**self.device.fields)
    info.update(**self.device.extra.fields)
    command = [ info.get('cmd')
              ]
    command.extend(info.get('args').split(' '))
    for opt in self.fields:
      if opt:
        command.append(getattr(args, opt))
    command.extend(getattr(args, 'remainder', []))
    command = shlex.split(' '.join(command))
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE)
    output, stderr = proc.communicate( )
    # output = check_output(command, shell=True)
    return output

