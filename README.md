# GatesMusicPet

A pet that can help you manage your music library.

### How to

Please see folder `ipynb` for details.

### Requriments

Install `ffmpeg` at [here](https://www.ffmpeg.org/download.html).

Install `flac` at [here](https://xiph.org/flac/download.html).

Install all python dependencies:

``` shell
pip install -r requirements.txt
```

### Known BUG

Windows and Linux environments are not tested.

### Following Plan

1. Create a module for FLAC helper class, which handles the parameter for the converting.
2. Modify the CUE class to a general Meta class, and it can load a CUE file.
3. Make this a site-package, with setup.py or something similar.
4. A manager with web interface, which can do search and mass copy to devices.

