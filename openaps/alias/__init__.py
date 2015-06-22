
import add, remove, show

from openaps.cli.subcommand import Subcommand
from openaps.cli.commandmapapp import CommandMapApp

from alias import Alias

def get_alias_map (conf):
  aliases = { }
  for alias in Alias.FromConfig(conf):
    aliases[alias.name] = alias
  return aliases

class AliasAction (Subcommand):
  def setup_application (self):

    self.aliases = get_alias_map(self.config)
    choices = self.aliases.keys( )
    choices.sort( )
    self.parser.add_argument('name', choices=choices)
    super(AliasAction, self).setup_application( )

class AliasManagement (CommandMapApp):
  """ aliases - manage alias configurations """
  Subcommand = AliasAction
  name = 'action'
  title = '## Alias Menu'
  def get_dest (self):
    return 'action'
  def get_commands (self):
    return [ add, remove, show ]

