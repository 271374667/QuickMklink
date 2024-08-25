import tkinter as tk


class Clipboard:
    @staticmethod
    def get_clipboard_text() -> str:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        try:
            clipboard_text = root.clipboard_get()
        except tk.TclError:
            clipboard_text = ""
        root.destroy()
        return clipboard_text

    @staticmethod
    def set_clipboard_text(text: str):
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root.clipboard_clear()  # 清空剪切板
        root.clipboard_append(text)  # 写入文本到剪切板
        root.update()  # 更新剪切板内容
        root.destroy()


if __name__ == '__main__':
    # print(Clipboard.get_clipboard_text())
    # Clipboard.set_clipboard_text("Hello, World!")
    print(Clipboard.get_clipboard_text())
