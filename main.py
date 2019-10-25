#!/usr/bin/env python
# *-* coding:utf8 *-*
# sky

import re
import os
import configparser
from bs4 import BeautifulSoup
import requests
import json

def get_dir(html_list, root_dir):
    for i in os.listdir(root_dir):
        i=f"{root_dir}/{i}"
        if os.path.isdir(i):
            get_dir(html_list, i)
        elif os.path.isfile(i) and i.endswith("html"):
            html_list.append(i)
    return html_list

def verify(result_dict):
    """
    result_dict={
        css_file1: text, 
        css_file2: text, 
        style0: text, 
        style1: text, 
        ...
    }

    result={
        html_file:{
            css1: "key1, key2", 
            css2: "key1, key2", 
            style0: "key1, key2", 
            style1: "key1, key2"
        }, 
        html_file:{
            css1: null,                 # null css文件不存在, http的css则无法正常访问
            css2: "key1, key2", 
            style0: "key1, key2", 
            style1: "key1, key2"
        }, 
    
    }
    """

    result_dict_temp=result_dict.copy()
    for key_name in result_dict_temp:
        text=result_dict[key_name]
        if text=="Not Found":
            key_list=text
        else:
            key_list=[]

            for i in re_word_rule:              # 关键字添加进列表
                i=f"\\b{i}\\b"
                r=re.search(i, text, re.I)
                if r is not None: 
                    key_list.append(r.group())

            for i in re_color_rule:             # 判断颜色添加进入列表
                key=f"\\b{i}\\b:(.*?);"         # background   ;
                color_result=re.findall(key, text, re.I)

                for j in color_result:
                    rgb=re.search("rgb\((.*?)\)", j, re.I)      # 判断rgb颜色
                    if rgb is not None:
                        key_list.append(rgb.group())
                        continue

                    hex_color=re.search("#(\w{6})|#(\w{3})", j, re.I)
                    if hex_color is not None:
                        key_list.append(hex_color.group())
                        continue

                    for color in color_word:
                        if re.search(color, j, re.I):
                            key_list.append(color)
            if len(key_list)!=0:
                key_list=[str(i) for i in key_list[:]]
                key_list=",".join(key_list)

        if len(key_list)==0:                    # 若未校验出问题, 则删除该条目
            result_dict.pop(key_name)
        else:
            result_dict[key_name]=key_list

    return result_dict

def rule(filename, ignore_css_list):
    with open(filename, "r") as f:
        text=f.read()
    soup=BeautifulSoup(text, "lxml")
    #soup=BeautifulSoup(text, "html.parser")
    link=soup.find_all("link")
    style=soup.find_all("style")

    html_dirname=os.path.dirname(filename)
    result={}                                       # 单文件dict
    for i in link:                                  # 判断href中的css文件类型, 并合成css文件的路径
        css_file=i.get("href")
        if css_file is not None:
            css_basename=os.path.basename(css_file)
            if css_file.endswith(".css") and css_basename not in ignore_css and "#" not in css_file:
                css_file=css_file.strip()
                if css_file.startswith("/"):            # 绝对路径开头
                    #css_file=f"{webapps}/{css_file}"
                    css_file=css_file[1:]
                    if os.path.exists(css_file):
                        with open(css_file) as f:
                            text=f.read()
                    else:
                        text="Not Found"
                elif css_file.startswith("http"):       # url
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
                    url=css_file
                    res=requests.get(url, headers=headers)
                    code=res.status_code
                    if code==200:
                        text=res.text
                    else:
                        text="Not Found"
                elif css_file.startswith(".") or css_file.startswith(".."): # 相对路径
                    css_file=f"{html_dirname}/{css_file}"
                    if os.path.exists(css_file):
                        with open(css_file) as f:
                            text=f.read()
                    else:
                        text="Not Found"
                if text!="":
                    css_file=os.path.normpath(css_file)
                    result[css_file]=text

    for index, item in enumerate(style):            # 将style里的css分别赋给style<n>
        result[f"style{index}"]="".join(item)

    if len(result)==0:                              # 判断是否有内容
        return result
    else:
        return verify(result)

def main():
    # 获取root_dir目录下所有html的文件路径
    html_list=[]
    all_html_list=get_dir(html_list, root_dir)

    # 排除掉ignore_dir目录的html
    if ignore_dir!="":
        for i in all_html_list[:]:
            for j in ignore_dir.split(","):
                j=f"{root_dir}/{j.strip()}"
                if i.startswith(j):
                    all_html_list.remove(i)

    # 排除掉ignore_html的html
    if ignore_html!="":
        for i in ignore_html.split(","):
            i=f"{root_dir}/{i.strip()}"
            if i in all_html_list:
                all_html_list.remove(i)

    ignore_css_list=[]
    if ignore_css!="":
        for i in ignore_css.split(","):
            ignore_css_list.append(i.strip())

    result_all={}
    for i in all_html_list:
        single_result=rule(i, ignore_css_list)
        if len(single_result)!=0:
            result_all[i]=single_result

    with open(f"{output}", "w") as f:
        json.dump(result_all, f)

if __name__ == "__main__":
    my_dir=os.path.abspath(os.path.dirname(__file__))
    os.chdir(my_dir)

    re_word_rule=["font-size", "padding", "padding-left", "padding-right", "padding-top", "padding-bottom"]
    re_color_rule=["color", "border-color", "border-top-color", "border-botton-color", "border-left-color", "border-right-color", "background-color", "background"]
    color_word=['aqua', 'limegreen', 'orchid', 'mediumpurple', 'powderblue', 'oldlace', 'burlywood', 'mistyrose', 'seashell', 'teal', 'honeydew', 'skyblue', 'violet', 'khaki', 'lightsalmon', 'dimgray', 'seagreen', 'pink', 'orangered', 'cadetblue', 'darkgreen', 'brown', 'whitesmoke', 'navy', 'papayawhip', 'purple', 'mediumturquoise', 'mediumaquamarine', 'hotpink', 'lightblue', 'paleturquoise', 'darkseagreen', 'mediumvioletred', 'mintcream', 'darkgoldenrod', 'greenyellow', 'olive', 'lightgreen', 'lightyellow', 'crimson', 'thistle', 'navajowhite', 'chartreuse', 'darkslategray', 'palevioletred', 'lime', 'lightslategray', 'orange', 'cornsilk', 'lavenderblush', 'lawngreen', 'goldenrod', 'yellowgreen', 'coral', 'turquoise', 'darkslateblue', 'darkturquoise', 'springgreen', 'forestgreen', 'sienna', 'darkorange', 'magenta', 'linen', 'lightskyblue', 'olivedrab', 'darkgray', 'deeppink', 'midnightblue', 'green', 'tomato', 'darkmagenta', 'lightgrey', 'darkorchid', 'peru', 'royalblue', 'tan', 'mediumblue', 'blueviolet', 'lemonchiffon', 'cornflowerblue', 'aliceblue', 'blanchedalmond', 'mediumspringgreen', 'beige', 'indianred', 'ghostwhite', 'peachpuff', 'darkcyan', 'azure', 'steelblue', 'lavender', 'moccasin', 'firebrick', 'mediumorchid', 'white', 'blue', 'lightseagreen', 'darkolivegreen', 'darkkhaki', 'mediumslateblue', 'palegreen', 'salmon', 'slategray', 'gainsboro', 'lightslateblue', 'ivory', 'red', 'mediumseagreen', 'rosybrown', 'darksalmon', 'lightcoral', 'plum', 'indigo', 'darkviolet', 'snow', 'gray', 'gold', 'violetred', 'lightpink', 'bisque', 'lightsteelblue', 'chocolate', 'fuchsia', 'black', 'feldspar', 'sandybrown', 'wheat', 'palegoldenrod', 'saddlebrown', 'darkblue', 'slateblue', 'dodgerblue', 'aquamarine', 'lightgoldenrodyellow', 'yellow', 'maroon', 'floralwhite', 'antiquewhite', 'cyan', 'darkred', 'deepskyblue', 'silver', 'lightcyan']

    cfg=configparser.ConfigParser()
    cfg.read("./re.ini")

    root_dir=cfg.get("re", "root_dir").strip()
    ignore_dir=cfg.get("re", "ignore_dir")
    ignore_html=cfg.get("re", "ignore_html")
    ignore_css=cfg.get("re", "ignore_css")
    output=cfg.get("re", "output").strip()

    work_dir=os.path.dirname(root_dir)
    os.chdir(work_dir)
    root_dir=os.path.basename(root_dir)
    main()
