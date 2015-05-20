# GatesMusicPet

A pet that can help you manage your music library.

### How to

Please see folder `ipynb` for details.

In the future, installing the package will create several commands.

### Requriments

Install `ffmpeg` at [here](https://www.ffmpeg.org/download.html).

Install `flac` at [here](https://xiph.org/flac/download.html).

Install all python dependencies:

``` shell
pip install -r requirements.txt
```

You can create a `virtualenv` as an isolated environment to install
the python packages:

``` shell
pip install virtualenv  # If you didn't installed before.
virtualenv env
source env/bin/activate
# here you are in virtualenv
pip install -r requirements.txt
```

### Known BUG

Windows and Linux environments are not tested.

### Following Plan

1. Make this a site-package, with setup.py or something similar. (In progress)
1. A manager with web interface, which can do search and mass copy to devices.
1. Getting album info with some API (e.g: VGMdb).


