# Set up development on Windows.

These steps were tested on a blank Windows 8.1 system. If you must work on
windows, this should help you get started.

## Download these packages:
* [Openssl][openssl], required by Mosquitto.
* The [Mosquitto MQTT broker][mosquitto]
* [Git][git], for checking our the source code.
* [Python 2.7][python]

## Install virtualenv

In a command window:

    c:\Python27\Scripts\pip.exe install virtualenv

## Check out the source and install dependencies

In an explorer window, in the location where you want to do your development,
right click and choose "Git bash here". You will now be in a shell that would
be familiar to all users of decent operating systems. Run these commands to
check out the source.

    git clone https://github.com/izak/ib.bluelantern.git
    cd ib.bluelantern
    /c/Python27/Scripts/virtualenv venv
    venv/Scripts/pip install -e .

## Start it all up

In another command window, run the MQTT broker.

    c:\Program Files\mosquitto\mosquitto.exe

Finally, in the git bash window, run:

    venv/Scripts/python scripts/simulate_load.py &
    venv/Scripts/python scripts/simulate_mppt.py &
    venv/Scripts/pserve.exe development.ini

Then open the [UI][bluelantern] in a browser. Presently it does not work in IE,
but IE is not a real browser.

## Shut it down

To kill the pyramid service, hit `ctrl+c`. To kill the backgrounded simulation
processes, type `jobs` to list them, then `fg` to bring to the forgeround, and
`ctrl+c` to stop.

## Follow the process
You can always get the latest version of the source code by opening a bash
shell and typing (inside the source folder):

    git pull

A discussion of git development processes is beyond the scope of this document.

[openssl]: https://slproweb.com/products/Win32OpenSSL.html
[mosquitto]: http://www.eclipse.org/downloads/download.php?file=/mosquitto/binary/win32/mosquitto-1.4.8-install-win32.exe
[git]: https://git-scm.com/download/win
[python]: https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi
[bluelantern]: http://localhost:6543/
