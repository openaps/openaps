
import init

builtins = {
  'init': init.init
  #,  'alias':
}
def dispatch (args, app):
  builtins.get(args.command)(args)

def is_builtin (command):
  if command in builtins:
    return True
  return False

