from pathlib import Path

# 配置proxy这样可以访问全部互联网
PROXY_URL = "http://127.0.0.1:7897"
APIS={}

PARENT_DIR = Path(__file__).parent.parent
APIS_DATA_NAME="apis_data.json"