
from ConfigParser import SafeConfigParser
import re


class Config (SafeConfigParser):
  OPTCRE = re.compile(
          r'\s?(?P<option>[^:=\s][^:=]*)'       # very permissive!
          r'\s*(?P<vi>[:=])\s*'                 # any number of space/tab,
                                                # followed by separator
                                                # (either : or =), followed
                                                # by any # space/tab
          r'(?P<value>.*)$'                     # everything up to eol
          )
  @classmethod
  def Read (klass, name=None, defaults=['openaps.ini', '~/.openaps.ini', '/etc/openaps/openaps.ini']):
    config = Config( )
    if name:
      config.read(name)
    else:
      config.read(defaults)
    return config


