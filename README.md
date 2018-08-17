# ximage


```
pip install ximage
```



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

    - pdftoppm: pdf ->  png

    - pdf2svg: pdf ->  svg

Options:
  --dpi INTEGER  the output image dpi
  --format TEXT  the output image format
  --help         Show this message and exit.
```

**Requirements:** 

- If you have **pillow**  module, then you can convert thats image format: png jpg gif tiff bmp ppm
- If you have install **pdftoppm** command which is come from the （if you in windows and you have installed the texlive ）`C:\texlive\2018\bin\win32\pdftoppm.exe`
- If you have install **Inkscape** then you can convert svg to pdf.
