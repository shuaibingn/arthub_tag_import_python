## ArtHub Tag Import GUI


### 使用

- GUI

使用python中的`tkinter`

- excel

在对excel操作时, 针对于`xlsx`格式的文件, 使用了`openpyxl`, `xls`主要使用了`xlutils`

- 编译exe

编译`exe`使用了`pyinstaller`

命令如下
```shell
pyinstaller.exe -w -F .\main.py
```

`-w`参数主要作用时在编译之后隐藏`cmd`终端

### 运行

使用时建议使用管理员权限运行程序, 因为存在对文件的写操作, 在某些电脑上可能没有权限
![以管理员身份运行](https://gitlab.h3d.com.cn/niushuaibing/arthub_tag_import_gui/blob/master/docs/%E4%BB%A5%E7%AE%A1%E7%90%86%E5%91%98%E8%BA%AB%E4%BB%BD%E8%BF%90%E8%A1%8C.png)