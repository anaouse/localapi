import readchar
from rich import print as rprint
from app.input_box import InputBox

def run_tui():
    input_box = InputBox()
    input_box.start()

    while True:
        try:
            key = readchar.readkey()
            submitted = input_box.feed(key)

            if submitted is not None and submitted.strip():
                if submitted == "quit":
                    break
                elif submitted == "clear":
                    input_box.clear()
                else:
                    rprint(f"[green]{submitted}[/green]")
                    input_box.start()

        except KeyboardInterrupt:
            rprint(f"\n[blue]Bye![/blue]")
            break


def main():
    run_tui()

if __name__ == "__main__":
    main()
