# 代码扫描工具
- 用于检查html代码中是否包含不符合规定的样式代码

## 说明
- 检查css样式中是否包含自定义的颜色, 内边距, 字体大小等样式
- 支持自定义检查目录
- 支持忽略子目录和文件
- 支持忽略自定义css名称

## 安装
```

```

## 使用
```
# cd re_html/
# vim re.ini
[re]
# 指定要扫描的目录, 需要绝对路径
root_dir=/data1/dsfa

# 指定要忽略的目录, 该目录相对于root_dir指定的目录, 多个目录以", "分隔
ignore_dir=WEB-INF, ueditor, dsfa/pd, dsfa/bhc/hc, res/dsf_styles, res/dsf_res, res/libs                                                                                     

# 指定要忽略的html文件, 该目录相对于root_dir指定的目录, 多个文件以", "分隔
ignore_html=A/B/haha.html

# 指定忽略的css文件名称, 以", "分隔
ignore_css=layui.css, zTreeStyle.css, dsf_style.css, iconfont.css, bhc.css, laydate.css, layer.css                                                                           

# 指定输出的文件名, 需用绝对路径
output=/data1/dsfa/output.json

```

## 样例结果说明 
```

```
