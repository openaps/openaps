
import os

def init (args):
  cmd = 'git-openaps-init'
  if args.args[1] == '--nogit':
    cmd = 'nogit-openaps-init'
  shell_cmd = [cmd ] + args.args
  os.execvp(shell_cmd[0], shell_cmd)

