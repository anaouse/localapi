import sys
import readchar
import unicodedata

def get_char_width(c: str) -> int:
    """获取单个字符的终端视觉显示宽度"""
    # 'W' (Wide) 和 'F' (Fullwidth) 通常占据 2 个终端列
    if unicodedata.east_asian_width(c) in ('F', 'W'):
        return 2
    return 1

def get_string_width(s: str) -> int:
    """获取字符串的总终端视觉显示宽度"""
    return sum(get_char_width(c) for c in s)

class InputBox:
    def __init__(self, prompt: str = "> "):
        self.text: str = ""
        self.cursor_pos: int = 0
        self.prompt = prompt
        self.history: list[str] =[]       # 已提交的历史命令
        self.history_index: int = -1       # -1 = 当前草稿，0 = 最新历史
        self.draft: str = ""               # 浏览历史时暂存当前输入

    def start(self):
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

    def _replace_line(self, new_text: str):
        """清除当前输入行，替换为 new_text，并更新状态。"""
        # 计算光标前面的文本实际占用的终端列宽
        visual_width = get_string_width(self.text[:self.cursor_pos])
        if visual_width > 0:
            sys.stdout.write(f"\033[{visual_width}D")
        
        # 清除从光标到行尾
        sys.stdout.write("\033[K")
        # 写入新内容
        sys.stdout.write(new_text)
        sys.stdout.flush()
        self.text = new_text
        self.cursor_pos = len(new_text)

    def feed(self, key: str) -> str | None:
        if key in (readchar.key.ENTER, "\r", "\n"):
            submitted = self.text
            if self.text != "clear":
                sys.stdout.write("\n")
                sys.stdout.flush()
            # 非空命令才记录历史，且不重复记录连续相同命令
            if submitted and (not self.history or self.history[0] != submitted):
                self.history.insert(0, submitted)   # 最新的放在最前面
            self.text = ""
            self.cursor_pos = 0
            self.history_index = -1                 # 重置历史指针
            self.draft = ""
            return submitted

        elif key == readchar.key.UP:
            if not self.history:
                return None
            next_index = self.history_index + 1
            if next_index >= len(self.history):
                return None                         # 已到最旧，不再往上
            if self.history_index == -1:
                self.draft = self.text              # 保存当前草稿
            self.history_index = next_index
            self._replace_line(self.history[self.history_index])

        elif key == readchar.key.DOWN:
            if self.history_index == -1:
                return None                         # 已在底部，无需操作
            self.history_index -= 1
            if self.history_index == -1:
                self._replace_line(self.draft)      # 恢复草稿
            else:
                self._replace_line(self.history[self.history_index])

        elif key in (readchar.key.BACKSPACE, "\x7f"):
            if self.cursor_pos > 0:
                # 获取将要删除的字符的显示宽度
                char_to_delete = self.text[self.cursor_pos - 1]
                w = get_char_width(char_to_delete)
                
                # 更新内部文本
                self.text = self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                self.cursor_pos -= 1
                
                # 终端光标左移实际视觉宽度
                sys.stdout.write(f"\033[{w}D")
                
                # 获取光标后的剩余文本并计算宽度
                tail = self.text[self.cursor_pos:]
                tail_w = get_string_width(tail)
                
                # 打印剩余文本，并用 \033[K 清除可能残留在行尾的旧字符（非常重要，防止中文残影）
                sys.stdout.write(tail + "\033[K")
                
                # 把光标退回到正确的位置
                if tail_w > 0:
                    sys.stdout.write(f"\033[{tail_w}D")
                sys.stdout.flush()

        elif key == readchar.key.LEFT:
            if self.cursor_pos > 0:
                # 检查左边这个字符的宽度
                w = get_char_width(self.text[self.cursor_pos - 1])
                self.cursor_pos -= 1
                sys.stdout.write(f"\033[{w}D")
                sys.stdout.flush()

        elif key == readchar.key.RIGHT:
            if self.cursor_pos < len(self.text):
                # 检查右边这个字符的宽度
                w = get_char_width(self.text[self.cursor_pos])
                self.cursor_pos += 1
                sys.stdout.write(f"\033[{w}C")
                sys.stdout.flush()

        elif key == readchar.key.HOME:
            w = get_string_width(self.text[:self.cursor_pos])
            if w > 0:
                sys.stdout.write(f"\033[{w}D")
                sys.stdout.flush()
                self.cursor_pos = 0

        elif key == readchar.key.END:
            w = get_string_width(self.text[self.cursor_pos:])
            if w > 0:
                sys.stdout.write(f"\033[{w}C")
                sys.stdout.flush()
                self.cursor_pos = len(self.text)

        elif len(key) == 1 and key.isprintable():
            # 更新内部文本
            self.text = self.text[: self.cursor_pos] + key + self.text[self.cursor_pos :]
            self.cursor_pos += 1
            
            # 不再使用 \033[@ 插入空缺，而是直接输出当前字符，再重绘光标后的内容
            sys.stdout.write(key)
            tail = self.text[self.cursor_pos:]
            
            if tail:
                sys.stdout.write(tail)
                # 把光标移回到刚才输入字符后的位置
                tail_w = get_string_width(tail)
                if tail_w > 0:
                    sys.stdout.write(f"\033[{tail_w}D")
                    
            sys.stdout.flush()

        return None

    def clear(self):
        """
        Clear both the visible screen and the scrollback buffer without flicker.
        """
        sys.stdout.write(
            "\033c"          # erase scrollback buffer
            "\033[H"         # move cursor to top-left (1,1)
        )
        self.start()