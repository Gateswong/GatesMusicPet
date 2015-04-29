## notebook `ConvertWholeTrackToFLACs`

### How To

Run `ipython notebook` in folder `ipynb`. Open `ConvertWholeTrackToFLACs.ipynb`.
Edit first cell, modify them to match your own situation.

``` python
WORKING_DIR = "Your Working Dir"
```

The working dir is the file that contains your music files. Typically, the whole
track file, and the CUE file.

``` python
FILENAME_PREFIX = "Filename prefix"
```

Make the files in the same prefix. For example, if your whole track file is `ABC.ape`,
make the cue sheet `ABC.cue` or `ABC.utf8.cue` (which to use? see below)

``` python
ANSI_ENCODING = "gbk"
```

If your cue file contains non-ACSII characters, modify this to match your CUE file encoding.
The converted file wil be saved as `ABC.utf8.cue` if your ANSI cue file is `ABC.cue`.

If your cue file is already utf8 encoded, save or rename the file as utf8 filename. 
(`ABC.utf8.cue` in this example)

``` python
OUTPUT_PREFIX = "output/"
```

You can give a absolute path here, then you can make all output files in the same folder, 
or a same base folder.

``` python
PICTURE = "cover.jpg"
```

If you have the cover picture for the album, set this value the same as your picture name.
If you don't have or don't need that, set this to `None`.

``` python
EXTRA_DATA_FILE = "%s.extra.ini" % FILENAME_PREFIX
```

You can save custom tags into this file (`ABC.extra.ini` in this example). For the
section `default`, the tag will equals the value if CUE don't have that field. For
the section `overwrite`, the tag will always equals to the value in the extra data
file.


