from tkinter import *
from tkinter import filedialog
import CrawlerGetJson
import CrawlerAnalysisJson
import os

def opendir():
    os.system('start' + " 洛谷题库")



window = Tk()
window.title("洛谷爬虫系统")
window.geometry("300x300")
button1 = Button(window, text="刷新题库",command = CrawlerGetJson.TCGJmain)
button1.pack()
button1 = Button(window, text="入门",command = lambda: CrawlerAnalysisJson.main(1))
button1.pack()
button2 = Button(window, text="普及-",command = lambda: CrawlerAnalysisJson.main(2))
button2.pack()
button3 = Button(window, text="普及/提高-",command = lambda: CrawlerAnalysisJson.main(3))
button3.pack()
button4 = Button(window, text="普及+/提高",command = lambda: CrawlerAnalysisJson.main(4))
button4.pack()
button5 = Button(window, text="提高+/省选-",command = lambda: CrawlerAnalysisJson.main(5))
button5.pack()
button6 = Button(window, text="省选/NOI-",command = lambda: CrawlerAnalysisJson.main(6))
button6.pack()
button7 = Button(window, text="NOI/NOI+/CTSC",command = lambda: CrawlerAnalysisJson.main(7))
button7.pack()
button7 = Button(window, text="打开文件所在位置", command = opendir)
button7.pack()

window.mainloop()