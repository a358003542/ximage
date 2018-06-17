# ximage
之前弄得图片处理命令行工具单独抽出来。



```
pip install ximage
```


提供了 ximage 这个命令，进一步有：
```
ximage resize ...
```

```
ximage convert ...
```

具体参数请使用 --help 查看之，后续文档补全。

convert 子命令 在windows下 最好 安装 inkscape 和 gimp 。

其中 inkscape 提供了对svg 文件 格式的支持。

gimp 提供了 pdftoppm ，可用来将 pdf 转成 png。

后续文档进一步补全。




## TODO
之前这两个命令只是之前一个小项目的一个小功能，现在开始认识到，将这两个图片处理，尤其是格式转换功能做完善，有太多的事情和问题要考虑了，

这个项目后面还有很多事情要做。