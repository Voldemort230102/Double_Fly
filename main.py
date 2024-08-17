from time import strftime
from os.path import exists
from os import mkdir
from tkinter import Tk,Toplevel,Label,Menu,Text,Scrollbar,RIGHT,LEFT,Y,END
from tkinter.messagebox import showerror,askquestion

# 各种函数
def void():
    print("void")
# 关闭
def quit_this(tk):
    tk.destroy()
    main()
# 记录日志
def put_log(file):
    # 设置你想检查的文件夹路径
    folder_path = "./log"
    file_path = folder_path + "/" + file
    # 检查文件夹是否存在
    if exists(folder_path):
        pass
    else:
        # 创建文件夹
        mkdir(folder_path)
        if exists(folder_path):
            pass
        else:
            # 无法创建的提示
            showerror("错误", "文件夹创建失败\n请前往目录手动创建")
            return
    # 检查文件是否存在
    if exists(file_path):
        pass
    else:
        # 创建文件
        open(file_path, "a",encoding="utf-8").close()
        if exists(file_path):
            pass
        else:
            # 无法创建的提示
            showerror("错误", "文件夹创建失败\n请前往目录手动创建")
            return
    # 读取文件
    f = open(file_path, "r", encoding="utf-8")
    data = f.read()
    f.close()
    time_data = strftime("%Y-%m-%d %H:%M:%S")
    # 如果data没有值
    if data == "":
        data = "1\n1:{}\n".format(time_data)
    # 如果data有值
    else:
        data = "{}\n{}{}:{}\nactivity:\n".format(str(int(data.split("\n")[0]) + 1), "\n".join(data.split("\n")[1:]),str(int(data.split("\n")[0]) + 1), time_data)
    # 写入
    f = open(file_path, "w", encoding="utf-8")
    f.write(data)
    f.close()
# 出库日志
def out_log():
    global home,width,height,win_width,win_height
    file_path = "./log/out_log.txt"
    try:
        f = open(file_path, "r", encoding="utf-8")
        data = f.read()
        f.close()
    except FileNotFoundError:
        # 创建文件
        open(file_path, "a", encoding="utf-8").close()
        if exists(file_path):
            pass
        else:
            # 无法创建的提示
            showerror("错误", "文件创建失败\n请前往目录手动创建")
            return
    home.destroy()
    show("出库日志", data, 1)
# 询问窗口
def ask(tk):
    tk.attributes("-disabled", 1)
    width = 235
    height = 140
    question = Toplevel(tk)
    question.title("")
    tk_width = tk.winfo_width()
    tk_height = tk.winfo_height()
    tk_x = tk.winfo_x()
    tk_y = tk.winfo_y()
    question.resizable(False,False)
    question.geometry("{}x{}+{}+{}".format(width, height, tk_x + int(tk_width / 2 - width / 2), tk_y + int(tk_height / 2 - height / 2)))
    question.transient(tk)
    question.protocol("WM_DELETE_WINDOW", void)

# 展示页面
def show(title, data, flag):
    global width,height,win_width,win_height
    # 创建窗口
    show_products = Tk()
    show_products.title(title)
    show_products.resizable(False,False)
    show_products.geometry("{}x{}+{}+{}".format(width, height, int(win_width / 2 - width / 2), int(win_height / 2 - height / 2)))
    show_products.iconbitmap('./icon/icon16.ico')
    if flag:
        # 滚动条与展示框
        show_scrollbar = Scrollbar(show_products)
        show_scrollbar.pack(side=RIGHT, fill=Y)
        show = Text(show_products, font=('kaiti', 20, 'bold'))
        show.pack(side=LEFT, fill=Y)
        show_scrollbar.config(command=show.yview)
        show.config(yscrollcommand=show_scrollbar.set)
        # 询问是否按编码特定查询
        if_flag = askquestion("提示","请问是否按编码特定查询")
        # 确认时
        if if_flag == "no":
            # 总数
            data = data.split("\n")
            show.insert(END, data[0] + '\n', 'total_tag')
            products = data[1:]
        else:
            data = data.split("\n")
            products = data[1:]
            products = "\n".join(products).split("\n\n")
            print(products)
            ask(show_products)
        # 字体
        for i in products:
            # 时间
            if "-" in i:
                show.insert(END, i + "\n", "time_tag")
            # 活动
            elif "activity:" in i:
                show.insert(END, i + "\n", "activity_tag")
            # 空
            elif "" == i:
                show.insert(END, "\n", "n_tag")
            # 产品
            else:
                mod = i.split(" ")[0]
                code = i.split(" ")[1]
                name = i.split(" ")[2]
                number = i.split(" ")[3]
                show.insert(END, mod + " ", "mod_tag")
                show.insert(END, code + " ", "code_tag")
                show.insert(END, name + " ", "name_tag")
                show.insert(END, number + "\n", "number_tag")
        # 设置颜色
        show.tag_config("total_tag", foreground="#000000")
        show.tag_config("activity_tag", foreground="#000000")
        show.tag_config("n_tag", foreground="#000000")
        show.tag_config("mod_tag", foreground="#009966")
        show.tag_config("code_tag", foreground="#FF0000")
        show.tag_config("name_tag", foreground="#000000")
        show.tag_config("number_tag", foreground="#9900FF")
        show.config(state='disable')
    else:
        pass
    show_products.protocol("WM_DELETE_WINDOW", lambda: quit_this(show_products))
    show_products.mainloop()
# 初始化
def init():
    global home
    if exists("./log"):
        pass
    else:
        mkdir("./log")
    log_path = "./log/{}_log.txt"
    file_path = ["out","in","new","delete"]
    for i in file_path:
        if exists(log_path.format(i)):
            pass
        else:
            open(log_path.format(i), "a", encoding="utf-8").close()
    information_path = "./information.xlsx"
    if exists(information_path):
        pass
    else:
        showerror("错误", "没有 information.xlsx 文件！")
        home.destroy()
        quit()
# 首页
def main():
    global home,width,height,win_width,win_height
    # 定义窗口长宽
    width = 900
    height = 600
    # 创建窗口
    home = Tk()
    # 获取电脑窗口长宽
    win_width = home.winfo_screenwidth()
    win_height = home.winfo_screenheight()
    # 将窗口设定为屏幕中心
    home.resizable(False,False)
    home.geometry('{}x{}+{}+{}'.format(width, height, int(win_width / 2 - width / 2), int(win_height / 2 - height / 2)))
    # 设置标题
    home.title('Double Fly')
    home.iconbitmap('./icon/icon16.ico')

    # 初始化
    init()

    # 创建菜单栏
    menu = Menu(home)
    home.config(menu=menu)

    # 添加一个"日志"菜单
    log_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="日志", menu=log_menu)
    log_menu.add_command(label="出库日志", command=lambda:out_log())
    log_menu.add_command(label="入库日志", command=void)
    log_menu.add_command(label="新建日志", command=void)
    log_menu.add_command(label="删除日志", command=void)

    # 添加一个"关于"菜单
    about_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="关于", menu=about_menu)
    about_menu.add_command(label="正版激活", command=void)
    about_menu.add_command(label="检查跟新", command=void)
    about_menu.add_separator()
    about_menu.add_command(label="关于我们", command=void)

    home.mainloop()

if __name__ == '__main__':
    main()