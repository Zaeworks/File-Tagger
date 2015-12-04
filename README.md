# File-Tagger
用标签标记文件/文件夹, 并用标签找到它们!

> 已经支持窗口化界面, 需依赖PyQt5库

> 在右键菜单为文件添加标签
> 通过在文件所在文件夹下添加.fileTagger文件实现记录文件/文件夹的标签
> 在FileTagger中通过标签搜索并快速打开它们

> Python 3.x (x86)
> 支持Windows32/64位系统, Linux下尚未测试

# 文件
         |         |
---------|---------|
fileTagger.py|本体
init_cmd.py|控制台入口(python下就是用它打开FileTagger啦)
reg.py|用于添加/移除右键菜单
setup.py|用于打包成控制台exe文件(依赖py2exe模块)

         |         |
---------|---------|
init_window.pyw|窗口化入口
dialog.py|包装ui_manage.py和ui_add.py
setup_window.py|用于打包成窗口化exe文件
ui/__init__.py|
ui/ui_add.py|快速标签界面
ui/ui_manage.py|管理界面


# 安装
### 获取FileTagger
#### 可执行版本(exe)
下载可执行版本: http://pan.baidu.com/s/1mgF7i7Q

> [C]为控制台版本, [W]为窗口化版本

或者获取代码手动打包

> setup.py 打包控制台版本 依赖py2exe
> setup_window.py 打包窗口化版本 依赖py2exe, PyQt5

> 控制台版本为单文件
> 窗口化版本因打包问题需要加载platforms/qwindow.dll, 请注意

#### Python版本
获取代码, 运行init_cmd.py或init_window.pyw

### 添加右键菜单(需管理员权限)

> 控制台版本下, 用管理员身份执行FileTagger.exe(或者管理员进入cmd => python init_cmd.py)
> 输入reg添加右键菜单, 输入unreg移除右键菜单

> 窗口化版本下, 管理员运行同上, 然后在下方勾选"添加右键菜单"

# 使用(窗口化版本)
对文件/文件夹/目录空白处点击右键即可进行对应的操作

窗口化版本易于使用不再详述

# 使用(控制台版本)
### 快速添加标签
在文件上点右键>添加/移除标签

默认为添加标签, 输入--r为移除指定标签

输入要添加或移除的标签, 用空格分隔

### 通过标签管理
在文件所在的目录下右键>标签式管理...

输入tag命令为目录添加标签, 或用其它命令管理资源

### 控制台命令
```
search (--or) 标签1 (标签2) (标签3...)
  - 在当前目录下搜索文件
	- 查找含指定标签的资源
	- 默认为and模式,输入--or参数进行or模式搜索
	- and模式:查找含有所有指定标签的资源
	- or模式:查找含有任一指定标签的资源
	- 返回一系列搜索结果,每项结果前有id,可以通过open命令快速打开
open id
	- 快速打开搜索结果中的指定资源
	- 使用默认打开方式打开文件,使用资源管理器打开文件夹
```
