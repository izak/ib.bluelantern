# Blue Lantern

Hope for the future.

TODO: Write this

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

    src/mosquitto -c mosquitto.conf
