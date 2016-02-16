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
is included below.

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
* [nodejs][node] to get the angular part working. This pulls in heaps of
  javascript libraries. In due course, I will probably aim at making a static
  distribution for people who don't want to develop this part.
* An MQTT broker. Instructions are included below for Mosquitto.

Some equipment requires specialised hardware.

* For Victron Multiplus and Quatro inverters you will need an MK2-USB module.
* For the Victron BlueSolar MPPT charge controllers equipped with a VE.Direct
  port, you will need the VE.Direct USB cable, or a similar USB to Serial (TTL
  level) converter. I strongly advise the use of the Victron cable for galvanic
  isolation.
* For the Victron BlueSolar 150/70 and 150/85, you will need a canbus
  interface. I own a 150/70, therefore I created an [arduino solution][arduino-victron-canbus]
  that converts the relevant info into VE.Direct.
* I hope that in due time this will also work with the popular Voltronic
  inverters.

## Detailed installation

TODO: write this.

## Install the angular part

To develop this part, you need [nodejs][node].

### Install Dependencies

We have two kinds of dependencies in this project: tools and angular framework code.  The tools help
us manage and test the application.

* We get the tools we depend upon via `npm`, the [node package manager][npm].
* We get the angular code via `bower`, a [client-side code package manager][bower].

We have preconfigured `npm` to automatically run `bower` so we can simply do:

```
npm install
```

Behind the scenes this will also call `bower install`.  You should find that you have two new
folders in your project.

* `node_modules` - contains the npm packages for the tools we need
* `app/bower_components` - contains the angular framework files

*Note that the `bower_components` folder would normally be installed in the
root folder but this is changed in the `.bowerrc` file.  Putting it in the app
folder makes it easier to serve the files by a webserver.*

## Install the python part

First install python and virtualenv. Then, to develop, change into the source
directory and:

    virtualenv venv
    venv/bin/pip install -e .

This will pull in all dependencies.

Start it with `venv/bin/pserve development.ini`

## Compile mosquitto

### Install requirements

    sudo apt-get install libwrap0-dev libssl-dev libuuid1-dev uuid-dev

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

[bower]: http://bower.io
[npm]: https://www.npmjs.org/
[node]: http://nodejs.org
[arduino-victron-canbus]: https://github.com/izak/arduino-victron-canbus
