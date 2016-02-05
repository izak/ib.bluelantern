# Blue Lantern

Hope for the future.

TODO: Write this

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

    src/mosquitto -c mosquitto.conf

[bower]: http://bower.io
[npm]: https://www.npmjs.org/
[node]: http://nodejs.org
