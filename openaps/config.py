
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
  ini_name = 'openaps.ini'
  def set_ini_path (self, ini_path='openaps.ini'):
    self.ini_name = ini_path
  def save (self):
    with open(self.ini_name, 'wb') as configfile:
      self.write(configfile)
  def add_device (self, device):
    section = device.section_name( )
    self.add_section(section)
    for k, v in device.items( ):
      self.set(section, k, v)
    if 'extra' in device.fields and getattr(device, 'extra', None):
      extra = Config( )
      extra.set_ini_path(device.fields['extra'])
      extra.add_section(section)
      for k, v in device.extra.items( ):
        extra.set(section, k, v)
      extra.save( )

  def remove_device (self, device):
    section = device.section_name( )
    self.remove_section(section)
  @classmethod
  def Read (klass, name=None, defaults=['openaps.ini', '~/.openaps.ini', '/etc/openaps/openaps.ini']):
    config = Config( )
    if name:
      config.set_ini_path(name)
      config.read(name)
    else:
      config.set_ini_path('openaps.ini')
      config.read(defaults)
    return config


