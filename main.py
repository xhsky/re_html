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
    """循环获取目录列表
    """
    for i in os.listdir(root_dir):
        i=f"{root_dir}/{i}"
        if os.path.isdir(i):
            get_dir(html_list, i)
        elif os.path.isfile(i) and i.endswith("html"):
            html_list.append(i)
    return html_list

def verify(text):
    keys_dict={}
    if text!="":                # 排除css文件为空的情况
        if text=="Not Found":
            keys_dict=text
        else:
            # 按行匹配
            text_list=text.split('\n')
            for key_word in re_word_rule:              # 关键字匹配
                if key_word not in keys_dict:
                    keys_dict[key_word]=[]
                for index, item in enumerate(text_list):
                    re_key=rf'(\b{key_word}\b\s*:(?:.*?))(?:;|}}|")'
                    key_result=re.findall(re_key, item, re.I)

                    for j in key_result:
                        key_dict={}
                        key, value=j.split(":")
                        key_dict['line']=index+1
                        key_dict['context']=value.strip()
                        keys_dict[key_word].append(key_dict)
                if len(keys_dict[key_word])==0:
                    keys_dict.pop(key_word)

            for key_word in re_color_rule:             # 颜色匹配
                if key_word not in keys_dict:
                    keys_dict[key_word]=[]
                for index, item in enumerate(text_list):
                    re_key=rf'(\b{key_word}\b\s*:(?:.*?))(?:;|}}|")'
                    color_result=re.findall(re_key, item, re.I)

                    for i in color_result:
                        color=None
                        rgb=re.search("rgb\((.*?)\)", i, re.I)      # 判断rgb颜色
                        hex_color=re.search("#(\w{6})|#(\w{3})", i, re.I)
                        if rgb is not None or hex_color is not None:
                            color=i
                        else:
                            for j in color_word:
                                if re.search(j, i, re.I):
                                    color=i
                                    break
                        
                        if color is not None:
                            key_dict={}
                            key, value=color.split(":")
                            key_dict['line']=index+1
                            key_dict['context']=value.strip()
                            keys_dict[key_word].append(key_dict)
                if len(keys_dict[key_word])==0:
                    keys_dict.pop(key_word)
    return keys_dict

def rule(filename, ignore_css_list):
    with open(filename, "r") as f:
        text=f.read()
    soup=BeautifulSoup(text, "lxml")
    #soup=BeautifulSoup(text, "html.parser")
    link=soup.find_all("link")
    #style=soup.find_all("style")

    # 将单个html文件内的所有css文件组成list, 且将html文件也添加
    html_filename_list=[filename, ]
    for i in link:
        css_file=i.get("href")
        if css_file is not None:
            css_file=css_file.strip()
            css_filename=os.path.basename(css_file)
            # 从列表中排除忽略的css文件
            if css_file.endswith(".css") and \
                    css_filename not in ignore_css and \
                    "#" not in css_file:
                        html_filename_list.append(css_file)

    result={}
    # 读取文件内容, 定义text=f.read()
    for i in html_filename_list:                                  
        if i.endswith(".css"): 
            if i.startswith("/"):               # 绝对路径开头
                i=i[1:]                         # 去掉"/"
                if os.path.exists(i):
                    with open(i, "r") as f:
                        text=f.read()
                else:
                    text="Not Found"
            elif i.startswith("http"):          # url
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
                res=requests.get(i, headers=headers)
                code=res.status_code
                if code==200:
                    text=res.text
                else:
                    text="Not Found"
            #elif css_file.startswith(".") or css_file.startswith(".."): # 相对路径
            else:
                i=f"{os.path.dirname(filename)}/{i}"
                if os.path.exists(i):
                    with open(i, "r") as f:
                        text=f.read()
                else:
                    text="Not Found"
        else:                                   # html文件
            with open(i, "r") as f:
                text=f.read()

        file_name=os.path.normpath(i)
        temp=verify(text)
        if len(temp)!=0:
            result[file_name]=temp
    return result

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

    # 格式化忽略的css(去掉前后空格)
    ignore_css_list=[]
    if ignore_css!="":
        for i in ignore_css.split(","):
            ignore_css_list.append(i.strip())

    # 按文件组织dict, 并写入json文件
    result_all={}
    for i in all_html_list:
        single_result=rule(i, ignore_css_list)
        if len(single_result)!=0:
            result_all[i]=single_result
    with open(f"{output}", "w") as f:
        json.dump(result_all, f)

if __name__ == "__main__":
    """
    result={
        html_file:{
            css1: {
                key1: [ { line: N, context: None }, { line: N, context: None } ], 
                key2: [ { line: N, context: None } ]
            }, 
            html: {
                key1: [ { line: N, context: None }, { line: N, context: None } ], 
                key2: [ { line: N, context: None } ]
            } 
        }, 
    }
    """
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
