import sys
import readchar

class InputBox:
    def __init__(self, prompt: str = "> "):
        self.text: str = ""
        self.cursor_pos: int = 0
        self.prompt = prompt

    def start(self):
        """Call once to draw the initial prompt."""
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

    def feed(self, key: str) -> str | None:
        """
        Process one key and update terminal in-place.
        Returns the submitted string on Enter, or None while still editing.
        """
        if key in (readchar.key.ENTER, "\r", "\n"):
            submitted = self.text
            if self.text != "clear":
                sys.stdout.write("\n")
                sys.stdout.flush()
            self.text = ""
            self.cursor_pos = 0
            return submitted

        elif key in (readchar.key.BACKSPACE, "\x7f"):
            if self.cursor_pos > 0:
                self.text = self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                self.cursor_pos -= 1
                sys.stdout.write("\033[D")  # move left
                sys.stdout.write("\033[P")  # delete char, pull rest left
                sys.stdout.flush()

        elif key == readchar.key.LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                sys.stdout.write("\033[D")
                sys.stdout.flush()

        elif key == readchar.key.RIGHT:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
                sys.stdout.write("\033[C")
                sys.stdout.flush()

        elif key == readchar.key.HOME:
            if self.cursor_pos > 0:
                sys.stdout.write(f"\033[{self.cursor_pos}D")  # jump left to start
                sys.stdout.flush()
                self.cursor_pos = 0

        elif key == readchar.key.END:
            if self.cursor_pos < len(self.text):
                remaining = len(self.text) - self.cursor_pos
                sys.stdout.write(f"\033[{remaining}C")        # jump right to end
                sys.stdout.flush()
                self.cursor_pos = len(self.text)

        elif len(key) == 1 and key.isprintable():
            self.text = self.text[: self.cursor_pos] + key + self.text[self.cursor_pos :]
            self.cursor_pos += 1
            sys.stdout.write("\033[@")  # open gap at cursor
            sys.stdout.write(key)       # fill it
            sys.stdout.flush()

        return None

    def clear(self):
            """
            Clear both the visible screen and the scrollback buffer without flicker.
            """
            sys.stdout.write(
                "\033c"        # erase scrollback buffer
                "\033[H"         # move cursor to top-left (1,1)
            )
            self.start()

