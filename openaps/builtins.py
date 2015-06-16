
import init
import alias
import shlex
import cli

from subprocess import call
class BuiltinApp (cli.ConfigApp):
  name = 'builtin'

builtins = {
  'init': init.init
}
class RunnableAlias (object):
  def __init__ (self, spec, parent):
    self.spec = spec
    self.parent = parent
  def __call__ (self, args):
    if self.spec is None:
      return None
    spec_command = self.spec.fields.get('command')
    cmd = 'openaps-%s' % spec_command
    if spec_command.startswith('!'):
      cmd = spec_command[1:]
    exit(call(shlex.split(cmd) + args.args))
def get_alias (command, app):
  spec = alias.get_alias_map(app.config).get(command, None)
  runnable = RunnableAlias(spec, app)
  return runnable

def dispatch (args, back):
  app = BuiltinApp(args)
  app.read_config( )
  builtins.get(args.command, get_alias(args.command, app))(args)

def is_builtin (command):
  app = BuiltinApp([ ])
  app.read_config( )
  if command in builtins:
    return True
  if command in alias.get_alias_map(app.config):
    return True
  return False

