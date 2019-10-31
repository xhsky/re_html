# 代码扫描工具
- 用于检查html代码中是否包含不符合规定的样式代码

## 说明
- 检查css样式中是否包含自定义的颜色, 内边距, 字体大小等样式
- 支持自定义检查目录
- 支持忽略子目录和文件
- 支持忽略自定义css名称
- 扫描结果保存在json文件中

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
  html_file_name1: {                                        # 扫描出的有问题的html文件名称
    html_file_name1: {                                      # html文件中的自定义语法
      key_name: [                                           # 关键字名称  
        {line: N, context: str},                            # 该关键字在文件中的行数(line)和内容(context)
        {line: N, context: str},
        ...
        ], 
      key_name: [
        {line: N, context: str}, 
        {line: N, context: str},
        ...
        ], 
      ...
    }
    css_file_name1: {                                       # html文件中css文件的自定义语法
      key_name: [                                           # 关键字名称  
        {line: N, context: str},                            # 该关键字在文件中的行数(line)和内容(context)
        {line: N, context: str},
        ...
        ], 
      key_name: [
        {line: N, context: str}, 
        {line: N, context: str},
        ...
        ], 
      ...
    }
    css_file_name2: "Not Found",                            # 若value为Not Found, 则表示该css文件路径有误,无法找到
    }, 
  ...
  }
```

- 实际文件
```
# output.json文件经格式化后的显示(默认存储为一行)
{
    "dsfa/dsfa/kit/styleDoc/index.html": {
        "dsfa/dsfa/kit/styleDoc/static/css/app.6453d1e7ee55665fdda7a6790afacb3f.css": {
            "background": [
                {
                    "context": "#ff0",
                    "line": 102
                },
                {
                    "context": "#23241f",
                    "line": 102
                }
            ],
            "border-left-color": [
                {
                    "context": "#000",
                    "line": 102
                },
                {
                    "context": "#999",
                    "line": 102
                },
                {
                    "context": "#fff",
                    "line": 102
                }
            ]
        }
    },
    "dsfa/dsfa/kit/styleDoc/static/zTree_v3/api/API_cn.html": {
        "dsfa/dsfa/kit/styleDoc/static/zTree_v3/api/API_cn.html": {
            "padding-top": [
                {
                    "context": "30px",
                    "line": 32
                }
            ]
        },
        "dsfa/dsfa/kit/styleDoc/static/zTree_v3/api/apiCss/common.css": {
            "background": [
                {
                    "context": "#528036 url(img/background.jpg) no-repeat fixed 0 0",
                    "line": 5
                },
                {
                    "context": "#262626",
                    "line": 121
                },
                {
                    "context": "#E8FCD6",
                    "line": 188
                }
            ]
        }
    }
    ...
}
```
