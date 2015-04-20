
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
  def save (self):
    with open('openaps.ini', 'wb') as configfile:
      self.write(configfile)
  def add_device (self, device):
    section = device.section_name( )
    self.add_section(section)
    for k, v in device.items( ):
      self.set(section, k, v)

  def remove_device (self, device):
    section = device.section_name( )
    self.remove_section(section)
  @classmethod
  def Read (klass, name=None, defaults=['openaps.ini', '~/.openaps.ini', '/etc/openaps/openaps.ini']):
    config = Config( )
    if name:
      config.read(name)
    else:
      config.read(defaults)
    return config


