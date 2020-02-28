#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import os
import os.path
import sys

import argcomplete
import openaps
from openaps import cli
from openaps.vendors import plugins


class VendorApp(cli.ConfigApp):
    """
  openaps-vendor - Manage vendor plugins.

    show    - lists all known vendors
    add     - add a new vendor
    remove  - remove a vendor
    """

    name = "plugins"

    def configure_parser(self, parser):
        self.read_config()
        self.configure_vendors()

    def configure_vendors(self):
        self.commands = plugins.VendorManagementActions(parent=self)
        self.commands.configure_commands(self.parser)

    def run(self, args):
        # print(self.commands)
        app = self.commands.selected(args)
        app(args, self)


if __name__ == "__main__":

    app = VendorApp(None)
    app()
