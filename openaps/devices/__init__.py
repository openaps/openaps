from openaps import vendors
from openaps.cli.subcommand import Subcommand

from . import add, remove, show
from .device import Device


def setup_application(app, parser):
    print("YYY CONFIG", app.config)
    pass


def get_devices(conf):
    return Device.FromConfig(vendors, conf)


def get_device_names(conf):
    return [device.name for device in Device.FromConfig(vendors, conf)]


def get_device_map(conf):
    devices = {}
    for device in Device.FromConfig(vendors, conf):
        devices[device.name] = device
    return devices


class DeviceConfig(Subcommand):
    def setup_application(self):
        choices = sorted(list(self.parent.devices.keys()))
        self.parser.add_argument("name", choices=choices)
        # self.devices = get_devices(self.parent.config)
        getattr(self.method, "configure_app", self._no_op_setup)(self, self.parser)


def configure_commands(parser, parent=None):
    subparsers = parser.add_subparsers(help="Operation", dest="command")
    commands = {}

    parent.devices = get_device_map(parent.config)
    for ctx in [add, remove, show]:
        app = DeviceConfig(ctx, parent=parent)
        parser = app.configure_subparser(subparsers)
        app.configure_parser(parser)
        commands[app.name] = app

    return commands


class Exported:
    Configurable = Device

    @classmethod
    def get_configurables(Klass, conf):
        return get_devices(conf)

    @classmethod
    def get_names(Klass, conf):
        return get_device_names(conf)

    @classmethod
    def get_map(Klass, conf):
        return get_device_map(conf)

    Command = DeviceConfig
