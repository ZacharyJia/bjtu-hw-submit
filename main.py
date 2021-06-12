import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
import requests
import os


class MainWindow:
    def __init__(self):
        self.win = Tk(className="北交大作业上传助手")
        self.win.geometry("600x250")

        datafile = "icon.ico"
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
        else:
            datafile = os.path.join(sys.prefix, datafile)

        self.win.iconbitmap(default=datafile)
        intro_label = Label(self.win, text="北交大课程平台采用Flash的方式上传作业附件，然而Flash"
                                           "目前已经停用，上传作业多有不便。因此扒了一下文件上传接口，写个小工具用来上传附件。\n"
                                           "使用方法：点击【选择文件】，选择要上传的作业，然后点击【上传文件】，将文件上传到课程平台。"
                                           "上传成功后，复制将下方输入框内的URL，以插入超链接的方式插入到作业输入框中。\n"
                                           "By Zachary    2021-06-12"
                            )
        intro_label.configure(wrap=550)
        intro_label.pack(pady=10)

        self.file_frame = Frame(self.win)
        self.label = Label(self.file_frame, text="已选文件:")
        self.label.pack(padx=10, side=LEFT)

        self.file_path = StringVar()
        self.file_path.set("请选择文件")
        self.file_label = Label(self.file_frame, textvariable=self.file_path)
        self.file_label.pack(fill=X, side=LEFT)

        self.file_frame.pack(pady=20, fill=BOTH)

        self.url = StringVar()
        self.url.set("上传后的URL")
        self.url_text = Entry(self.win, textvariable=self.url, width=80)
        self.url_text.pack()

        self.btn_frame = Frame(self.win)

        self.btn_choose = Button(self.btn_frame, text="选择文件", command=self.choose_file)
        self.btn_choose.pack(padx=30, side=LEFT)

        self.btn_submit = Button(self.btn_frame, text="上传文件", command=self.submit_file)
        self.btn_submit.pack(padx=30, side=RIGHT)

        self.btn_frame.pack()

    def show(self):
        self.win.mainloop()

    def choose_file(self):
        filepath = tkinter.filedialog.askopenfilename(title="选择要上传的文件")
        self.file_path.set(filepath)
        pass

    def submit_file(self):
        if not os.path.exists(self.file_path.get()):
            tkinter.messagebox.showerror(title='上传文件', message='选择的文件不存在!')
            return

        url = "http://cc.bjtu.edu.cn:81/meol/servlet/SerUpload"
        payload = {'folder': '/uploads'}
        files = [
            ('Filedata', (os.path.basename(self.file_path.get()), open(self.file_path.get(), 'rb')))
        ]
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code != 200:
            tkinter.messagebox.showerror(title='上传文件', message='上传失败，请稍后再试！')
            return
        print(response.text)

        self.url.set("http://cc.bjtu.edu.cn:81/meol/" + response.text)
        tkinter.messagebox.showinfo(title='上传文件', message='上传成功！')


def main():
    main_window = MainWindow()
    main_window.show()


if __name__ == '__main__':
    main()
