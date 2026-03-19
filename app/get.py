from rich import print as rprint
import asyncio
import aiohttp
from app.myglobal import PROXY_URL, APIS

def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

async def get(url):
    """
    直接用aiohttp方便之后可能的异步操作
    """
    async with aiohttp.ClientSession() as session:
        try:
            url = normalize_url(url)
            async with session.get(url, proxy=PROXY_URL, timeout=10) as response:
                try:
                    result = await response.json()
                except:
                    result = await response.text()
                rprint(f"[bold green]状态码:[/bold green] {response.status}")
                rprint(result)
        except Exception as e:
            rprint(f"[bold red]错误:[/bold red] {e}")

async def use_api(name: str):
    """
    根据配置中的 name 直接调用对应的接口
    """
    # 1. 从 APIS 字典获取配置
    api_config = APIS.get(name)
    if not api_config:
        rprint(f"[bold red]错误:[/bold red] 未找到名为 '{name}' 的接口配置")
        return

    method = api_config.get("method", "get").lower()
    url = api_config.get("url")
    if not url:
        rprint(f"[bold red]错误:[/bold red] 接口 '{name}' 缺少 url 配置")
        return

    rprint(f"[bold blue]正在请求接口:[/bold blue] {name} ({url})")
    if method == "get":
        await get(url)
    else:
        rprint(f"[bold yellow]提示:[/bold yellow] 目前仅支持 get 方法，该接口定义为 {method}")
