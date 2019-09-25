# ximage


```
pip install ximage
```

## changelog
### 0.2.0
1. change use pdf2ppm to pdftocairo, it can convert pdf to png|jpeg|svg etc.
2. the pip installation will make sure you have installed the pillow module.
3. the pip installation in windows will check is there have pdftocairo.exe, if can not found , program will copy the pdftocairo.exe to the python scripts folder.


## resize image
need the pillow module.

```
ximage resize ...
```

```
Usage: ximage resize [OPTIONS] INPUTIMGS...

  resize your image, width height you must give one default is zero. out
  :param inputimgs: 
  :param width: 
  :param height: 
  :param outputdir: 
  :param outputname:

Options:
  --width INTEGER    the output image width
  --height INTEGER   the output image height
  --outputdir TEXT   the image output dir
  --outputname TEXT  the image output name
  --help             Show this message and exit.

```

## convert image format
If you in windows , please install the inkscape and gimp software.


```
ximage convert ...
```

```
Usage: ximage convert [OPTIONS] INPUTIMGS...

  support image format:

    - pillow : png jpg gif eps tiff bmp ppm

    - inkscape: svg ->pdf  png ps eps

    - pdftocairo: pdf ->  png jpeg ps eps svg

Options:
  --dpi INTEGER  the output image dpi
  --format TEXT  the output image format
  --help         Show this message and exit.
```

