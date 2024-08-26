import tkinter as tk
from tkinter import messagebox


class MessageDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口

    def info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def confirm(self, title: str, message: str) -> bool:
        return messagebox.askokcancel(title, message)

    def __del__(self):
        self.root.destroy()


if __name__ == '__main__':
    dialog = MessageDialog()
    dialog.info('提示', '这是一个提示信息')
    dialog.warning('警告', '这是一个警告信息')
    dialog.error('错误', '这是一个错误信息')
    print(dialog.confirm('确认', '这是一个确认信息'))
