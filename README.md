
# openaps utility belt

These are the [core utilities][proposal] needed to develop an open source
artificial pancreas.

See our [wiki for more information][wiki], including how to
[get started with openaps][GettingStarted].

[GettingStarted]: https://github.com/openaps/openaps/wiki/GettingStarted
[wiki]: https://github.com/openaps/openaps/wiki
[proposal]: https://gist.github.com/bewest/a690eaf35c69be898711

This is not an artificial pancreas, but rather tools which independently allow:

* monitor - Collect data about environment, and operational status of devices.
  Aggregate as much data relevant to therapy as possible into one place.
  We propose a tool, `openaps-get` as a proof of concept.

* predict - Can make predictions about what should happen next.

* control - Can enact changes in the world: emails, placing phone calls, SMS,
  issuing commands to pumps.


## Install

See [GettingStarted][GettingStarted] for more important information
about versions of software dependencies, but to install from source
clone this repo, and issue:

    sudo  python setup.py develop


### Usage

    usage: openaps [-h] [-c C C] [-C CONFIG] [--version] [command] ...

#### openaps - openaps: a toolkit for DIY artificial pancreas system

##### positional arguments:
  * command
  * args

optional arguments:

    -h, --help            show this help message and exit
    -c C C
    -C CONFIG, --config CONFIG
    --version             show program's version number and exit

  Utilities for developing an artificial pancreas system.
  openaps helps you manage and structure reports for various devices.

## Common workflows:

    openaps init
    openaps device <cmd>
      
      Device commands allow you to match a device driver, with a name
      and a configuration.
      
      add     - add device config to `openaps.ini`
      remove  - remove device from `openaps.ini`
      show    - print device uri, list all by default

    openaps use [--format <json,stdout,text>]
                [--output <filename>]
            <device>
            <use>
            [use-args...]

      For each device registered, the vendor implementation provides a
      number of uses.  This allows users to experiment with reports.

    openaps report <cmd>

      Reports match a device use to a format and filename.

      add     - add report config to `openaps.ini`
      remove  - remove report from `openaps.ini`
      show    - print report uri, list all by default
      invoke  - run and save report in file

### Init new openaps environment

Setup of new instance:  

    openaps init <name>    - create a new instance of openaps
    openaps init myopenaps - this creates an instance of openaps in a new
                             directory, called myopenaps

    cd myopenaps - change directory to root of new repo

A valid instance of openaps is a git repo with a file called
`openaps.ini` present.

`openaps` will track configuration and some status information inside of
`openaps.ini`.

### Init existing git repo as openaps-environment 
If you already have a git repo which you would like to
become a valid openaps environent, in the root of your repo, run:

    touch openaps.ini
    git add openaps.ini
    git commit -avm 'init openaps'

Now, wth a valid `openaps` environment, you can register devices for
use.  A device is implemented by a vendor.  `openaps` [will] provide a
modular, language and process independent environment for creating
vendors and devices, but for now the only two are dexcom and
medtronic.

### Managing devices

To register devices for use, see `openaps device` commands:

    openaps device -h
    openaps device add <name> <vendor> [opts...]
    eg:
    # register a medtronic device named pump
    openaps device add pump medtronic 665455
    # register a dexcom device named cgm
    openaps device add cgm dexcom

### Using devices
Now that devices are known, and we have a variety of commands
available.  We can explore how to produce reports by using devices
with the `openaps use` command:

    openaps use <device-name> <use-name> [opts]

`openaps use` commands can only be used after devices have been added to
the `openaps.ini` config using `openaps device add`.
Eg:

    openaps use pump -h        - show available commands for the
                                 device known as "pump"
    openaps use pump iter_pump - get last 100 pump history records
                                 from the device called pump
    openaps use cgm -h         - show available commands for the
                                 device known as "cgm"
    openaps use cgm glucose

### Save reports
After experimenting with `openaps use` commands, users can save reports
using the `openaps report` commands.
`openaps report` commands map `openaps use` commands to filenames:

    openaps report add <report-name> <report-formatter> <device> <use> [opts]

    # add a report, saved in a file called pump-history.json, which is
    # JSON format, from device pump using use iter_pump.
    openaps report add pump-history.json JSON pump iter_pump

    # add a report, saved in a file called glucose.json, which is
    # JSON format, from device cgm using use glucose.
    openaps report add glucose.json JSON cgm glucose

    # invoke the report to create glucose.json
    openaps report invoke glucose.json

    # invoke the report to create pump-history.json
    openaps report invoke pump-history.json

All commands support tab completion, and -h help options to help
explore the live help system.


##### Sample `use` commands

###### `medtronic`

Assuming device is named `pump`:

    usage: openaps-use pump [-h]
                            {Session,status,read_clock,iter_pump,read_current_history_pages,read_temp_basal,reservoir,settings,mytest,scan,iter_glucose,read_current_glucose_pages,read_history_data,read_carb_ratios,read_settings,model,read_glucose_data}
                            ...

    positional arguments:
      {Session,status,read_clock,iter_pump,read_current_history_pages,read_temp_basal,reservoir,settings,mytest,scan,iter_glucose,read_current_glucose_pages,read_history_data,read_carb_ratios,read_settings,model,read_glucose_data}
                            Operation
        Session             session for pump
        status              Get pump status
        read_clock          Read date/time of pump
        iter_pump           Read latest 100 records
        read_current_history_pages
                            Read current history pages.
        read_temp_basal     Read temporary basal rates.
        reservoir           Get pump remaining insulin
        settings            Get pump settings
        mytest              Testing read_settings
        scan                scan for usb stick
        iter_glucose        Read latest 100 records
        read_current_glucose_pages
                            Read current glucose pages.
        read_history_data   Read pump history page
        read_carb_ratios    Read carb_ratios.
        read_settings       Read settings.
        model               Get model number
        read_glucose_data   Read pump glucose page

    optional arguments:
      -h, --help            show this help message and exit

###### `dexcom`

    usage: openaps-use cgm [-h] {glucose,scan} ...

    positional arguments:
      {glucose,scan}  Operation
        glucose       glucose
        scan          scan for usb stick

    optional arguments:
      -h, --help      show this help message and exit

