# 代码扫描工具
- 用于检查html代码中是否包含不符合规定的样式代码

## 说明
- 检查css样式中是否包含自定义的颜色, 内边距, 字体大小等样式
- 支持自定义检查目录
- 支持忽略子目录和文件
- 支持忽略自定义css名称

## 安装(Centos7.5)
1. 安装python3环境
```
# yum install python3 python3-devel git
```

2. 下载扫描工具
```
# cd /opt/
# git clone https://github.com/xhsky/re_html.git
```

3. 安装依赖
```
# cd /opt/re_html
# pip3 install -r requirements.txt
```

## 使用
1. 进入re_html目录, 并编辑配置文件re.ini
```
# cd /opt/re_html/
# vim re.ini
     [re]
     # 指定要扫描的目录, 需要绝对路径
     root_dir=/data1/dsfa
     
     # 指定要忽略的目录, 该目录相对于root_dir指定的目录, 多个目录以","分隔
     ignore_dir=WEB-INF, ueditor, dsfa/pd, dsfa/bhc/hc, res/dsf_styles, res/dsf_res, res/libs                                                                                     
     
     # 指定要忽略的html文件, 该目录相对于root_dir指定的目录, 多个文件以","分隔
     ignore_html=A/B/haha.html
     
     # 指定忽略的css文件名称, 以","分隔
     ignore_css=layui.css, zTreeStyle.css, dsf_style.css, iconfont.css, bhc.css, laydate.css, layer.css                                                                           
     
     # 指定输出的文件名, 需用绝对路径
     output=/data1/dsfa/output.json
```

2. 执行main.py, 开始扫描. 结果生成为json格式, 并保存在配置文件定义的output文件中
```
# ./main.py
```

## 样例结果说明 
- 样例语法
```
{
  html_file_name: {                                       # 扫描出的有问题的html文件名称
    css_file_name1: "自定义语法1, 自定义语法2",           # html文件中的css文件名及其中的自定义语法
    css_file_name2: "自定义语法1, 自定义语法2", 
    css_file_name3: "Not Found",                          # 若value为Not Found, 则表示该css文件无法找到
    style0: "自定义语法1, 自定义语法2",                   # html文件中的style格式, 若有多个style, 则从序号0开始.
    style1: "自定义语法1, 自定义语法2",
    }, 
  ...
  }
```

- 实际文件
```
# cat output.json
{
  "dsfa/dsfa/quartz/views/cron.html": {
      "dsfa/dsfa/quartz/res/cron/icon.css": "red",
      "dsfa/dsfa/quartz/res/cron/themes/bootstrap/easyui.min.css": "font-size: 12px;,padding: 5px;,padding-left: 18px;,padding-right: 0px;,padding-top: 2px;,padding-bo
      "dsfa/dsfa/quartz/res/cron/themes/icon.css": "red",
      "style0": "padding-left: 25px;,padding-left: 25px;"
  }
  "dsfa/dsfa/rm/views/rm.html": {
    "dsfa/dsfa/rm/res/rm.css": "font-size:16px;,padding:0 20px;,lightblue,#fff,#393D49,lightblue,#393D49"
  },
  "dsfa/dsfa/wf/views/flow_index.html": {
    "dsfa/dsfa/wf/res/css/easyui1.4.1/icon.css": "red,red,tan,blue,red",
    "dsfa/dsfa/wf/res/css/easyui1.4.1/themes/gray/easyui.css": "font-size: 12px;,padding: 5px;,padding-left: 18px;,padding-right: 0px;,padding-top: 2px;,padding-bott
    "dsfa/dsfa/wf/res/css/flow.css": "font-size:13px;,padding:5px;,#5B9BD5,#ffffff,#FFFFFF,#eaeaea,#eaeaea,#eaeaea,#e9f9ff,#e9f9ff,#fff,#f7f7f7,#999,#fff,#999,#fff,#
    "dsfa/dsfa/wf/res/css/systemskins/dsfa/themes/gray/DSSkin.css": "font-size:12px;,padding:2px 1px 2px 1px;,#ebeced,gray,#0C6699,#223c75,#d90000,gray,#ebeced,#F4F4
    "style0": "font-size: 12px !important;,#fff",
    "style1": "#CCEEFF,#CCEEFF"
  }
...
...
}
```
