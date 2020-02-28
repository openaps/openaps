#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import sys

import argcomplete
import openaps
from openaps import cli, devices, reports, uses


class ReportToolApp(cli.ConfigApp):
    """ openaps-report - configure reports

  Manage which devices produce which reports.

  Example workflow:

  Use the add, remove, show to manage which reports openaps knows about.

    The add command adds a new report to the system.
    The syntax is: add <name> <reporter> <device> <use>

      openaps report add my-results.json json pump basals

      This example registers a json output, using the pump basals command, and
      stores the result in my-results.json.

    The show command will list or give more details about the reports registered with openaps.
    The syntax is: show [name]. The default name is '*' which should list all available reports.

      openaps report show

    The remove command removes the previously configured report from openaps.
    The syntax is: remove <name>

      openaps report remove my-results.json
      This example removes the report "my-results.json" from the openaps
      environment.

    openaps report invoke basals
                   <action> <name>


    """

    name = "report"

    def configure_parser(self, parser):
        self.read_config()
        available = devices.get_device_map(self.config)
        self.devices = available
        choices = sorted(list(available.keys()))
        self.parser.add_argument(
            "--version",
            action="version",
            version="{} {}".format("%(prog)s", openaps.__version__),
        )

        self.configure_reports()

    def configure_reports(self):
        self.actions = reports.ReportManagementActions(parent=self)
        self.actions.configure_commands(self.parser)

    def configure_devices(self):
        allowed = []
        self.commands = uses.UseDeviceCommands(self.devices, parent=self)
        self.commands.configure_commands(self.parser)

    def prolog(self):
        super().prolog()

    def epilog(self):
        super().epilog()

    def run(self, args):
        # print(self.inputs)
        # print(args)
        app = self.actions.selected(args)
        output = app(args, self)
        # print(output)


if __name__ == "__main__":

    app = ReportToolApp(None)
    app()
