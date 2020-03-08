
import tkinter as tk
from core import BackupEngine


def callback():

    account = input_text.get()
    if account == '':
        print("请先输入QQ账号")
        return
    engine = BackupEngine(account, save_dir='./QQZone', headless=True)
    try:
        engine.download_images()
        engine.download_posts()
        engine.download_leaving_message()
        engine.download_diary()
    except Exception as e:
        print(e)
    finally:
        engine.finished()


window = tk.Tk()
window.title('QQ空间备份')
input_text = tk.Entry(window)
button = tk.Button(window, text='一键备份', command=callback)
input_text.pack()
button.pack()
tk.mainloop()