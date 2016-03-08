# Blue Lantern

Blue Lantern is a modular renewable energy monitoring system, or at least, with
enough time and effort it will be. It is named after the Blue Lantern Corps
organisation that appears in DC comics, not because I'm a fan of DC comics,
but because the the emotion of hope for the future on which it is based seems
apt when it comes to renewable energy.
Hope for the future.

## Components

One of design criteria was that it should be easy for a developer to interface
with a new piece of equipment by writing only the code necessary for
communicating with the relevant piece of equipment. Ideally it should be
possible for the developer to use the language of his choice.

For a communications bus, MQTT is utilised. Instructions for building Mosquitto
are included below.

In order to link your equipment, all you need to do is write the interfacing
code for communicating voltage, current and power (if available) onto the mqtt
bus, where other components will subscribe to the information they require
to operate.

For a start, it will support Victron Multiplus inverters, and the Victron
MPPT charge controllers, for no other reason than because that is what I have
available.

The other components of the system are:

* A web server, written in python and pyramid, that collects the related
  charge and discharge values, and aggregates it into a json stream for display
  use in a web application.
* A web application, using angularjs, for displaying gauges and providing other
  functions (currently still very crude and not at all useable yet).
* A logging component that will log power values to a local or remote database
  (not yet implemented).

For development you will need:

* Python, and preferably virtualenv.
* If you intend in-depth development on the web interface, you need
  [nodejs][node] to get the angular part working. This pulls in heaps of
  javascript libraries. This part is optional.
* An MQTT broker. Instructions are included below for Mosquitto.

Some equipment requires specialised hardware.

* For Victron Multiplus and Quatro inverters you will need an MK2-USB module.
* For the Victron BlueSolar MPPT charge controllers equipped with a VE.Direct
  port, you will need the VE.Direct USB cable, or a similar USB to Serial (TTL
  level) converter. I strongly advise the use of the Victron cable for galvanic
  isolation.
* For the Victron BlueSolar 150/70 and 150/85, you will need a canbus
  interface. I own a 150/70, therefore I created an
  [arduino solution][arduino-victron-canbus] that converts the relevant info
  into VE.Direct.
* I hope that in due time this will also work with the popular Voltronic
  inverters.

## Install the python part

First install python and virtualenv. Then, to develop, change into the source
directory and:

    virtualenv venv
    venv/bin/pip install -e .

This will pull in all dependencies and install the in the virtual environment,
leaving your original python installation unchanged.

Start it with `venv/bin/pserve development.ini`

## Compile mosquitto

This step is optional, although a working MQTT server is required. You can use
iot.eclipse.org for development or testing purposes, or you can use an
alternative broker available for your platform. Mosquitto is free, has few
dependencies, and works well for development.

### Install requirements

    sudo apt-get install libwrap0-dev libssl-dev uuid-dev

### Get mosquitto source

    git clone \
      http://git.eclipse.org/gitroot/mosquitto/org.eclipse.mosquitto.git \
      mosquitto

OR

    wget http://www.eclipse.org/downloads/download.php?file=/mosquitto/source/mosquitto-1.4.7.tar.gz
    tar zxf mosquitto-1.4.7.tar.gz

### Compile

Change into source directory, edit config.mk:

1. set WITH_SRV:=no (or alternatively install libc-ares-dev)
2. set WITH_DOCS:=no (or alternatively install docbook-xsl)

    make

### Restrict mqtt to localhost

Edit mosquitto.conf and set:

    bind_address 127.0.0.1

### Start it up

You can start mosquitto without installing it, if you just want to use it for
development.

    src/mosquitto -c mosquitto.conf

Likewise, you can use the utilities that comes with it, but for that to work
the library must be loadable. You can work around this by setting `LD_LIBRARY_PATH`.

    LD_LIBRARY_PATH=lib client/mosquitto_pub -t battery01/inverter/power -m 555.42

## Install the angular part

You don't need to do this unless you intend to do heavy development involving
the upstream dependencies. Everyone else can skip this as the code comes
prepackaged with a version of angular and all support libraries.

To develop this part, you need [nodejs][node]. After installing nodejs,
running `npm install` is sufficient to set up all the required components.

## Configuring components

### Victron MK2 inverter

Add lines similar to the below to your development.ini file. The port setting
relies on udev symlinking your usb-serial ports by their ids.  This is the
default setup on most Linux distributions and should work straight out of the
box.

    pyramid.includes =
        ib.bluelantern.victron.mk2

    mk2.instance = battery01
    mk2.name = inverter
    mk2.port = /dev/serial/by-id/usb-VICTRONENERGY_MK2USB_COM_Interface_FTABCDEF-if00-port0

### Victron BlueSolar MPPT

Add lines similar to below to your development.ini file.

    pyramid.includes =
        ib.bluelantern.victron.vedirect

    vedirect.instance = battery01
    vedirect.name = mppt
    vedirect.port = /dev/serial/by-id/usb-Silicon_Labs_CP2103_USB_to_UART_Bridge_Controller_0001-if00-port0

[bower]: http://bower.io
[npm]: https://www.npmjs.org/
[node]: http://nodejs.org
[arduino-victron-canbus]: https://github.com/izak/arduino-victron-canbus
