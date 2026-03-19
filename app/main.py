import readchar
from rich import print as rprint
import asyncio
from app.input_box import InputBox
from app.get import get, use_api
from app.data import load_apis, add_api, store_apis, show_apis
from app.myglobal import APIS

def input_router(submitted: str):
    """
    command format:
    get url
    add name method url description
    """
    command = submitted.split()
    if command[0] == "get":
        asyncio.run(get(command[1]))
    if command[0] == "add":
        add_api(*command[1:5])
    if command[0] == "show":
        show_apis()
    if command[0] == "use":
        asyncio.run(use_api(command[1]))



def run_tui():
    input_box = InputBox()
    input_box.start()

    while True:
        try:
            key = readchar.readkey()
            submitted = input_box.feed(key)

            if submitted is not None and submitted.strip():
                if submitted == "/clear":
                    input_box.clear()
                else:
                    input_router(submitted)
                    input_box.start()

        except KeyboardInterrupt:
            rprint(f"\n[blue]Bye![/blue]")
            store_apis()
            break


def main():
    load_apis()
    run_tui()

if __name__ == "__main__":
    main()
