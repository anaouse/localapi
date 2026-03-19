import json
from pathlib import Path
from app.myglobal import APIS, PARENT_DIR, APIS_DATA_NAME
from rich import print as rprint


def load_apis():
    """
    加载本地api文件，放到全局列表APIS里面
    """
    global APIS
    apis_file = PARENT_DIR / APIS_DATA_NAME
    if apis_file.exists():
        with open(apis_file, "r", encoding="utf-8") as f:
            APIS.update(json.load(f))

def add_api(name: str, method: str, url: str, description: str = ""):
    """
    添加一个api到APIS
    "name" : {
        "method": "get",
        "url": "https:127.0.0.1:8000/report/latest",
        "description": "我个人后端的一个接口"
    }
    name必须唯一，method和url必填，description可有可无
    """
    if name in APIS:
        print(f"API名称 '{name}' 已存在，name必须唯一")
        return
    if not method or not url:
        print("method 和 url 为必填项")
        return
    
    APIS[name] = {
        "method": method.lower(),
        "url": url,
        "description": description,
    }

    print(f"add api {name} successfully")
    print(f"method: {method}")
    print(f"url: {url}")
    print(f"description: {description}")
    store_apis()




def store_apis():
    """
    存储APIS json文件到本地: __file__.parent.parent / api_data.json 
    {
        "my_finance_report" : {
            "method": "get",
            "url": "http://127.0.0.1:8000/report/latest",
            "description": "这个是我的个人后端的一个接口
        },
        "xxx": {
            ...
        }
    }
    """
    apis_file = PARENT_DIR / APIS_DATA_NAME
    with open(apis_file, "w", encoding="utf-8") as f:
        json.dump(APIS, f, ensure_ascii=False, indent=4)

def show_apis():
    rprint(APIS)