import os
import tkinter as tk
import tkinter.filedialog as tkfile
from method import filter_file_path


class MyWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("筛选数据")
        self.path = tk.StringVar()
        self.path.set(os.path.abspath(".."))

        # 选择文件路径
        self.pathLabel = tk.Label(self.root, text="文件路径:")
        self.pathLabel.grid(row=0, column=0)
        self.pathText = tk.Entry(self.root, textvariable=self.path, state="readonly")
        self.pathText.grid(row=0, column=1)
        self.selectPathButton = tk.Button(self.root, text="选择路径", command=self._select_path)
        self.selectPathButton.grid(row=0, column=2)

        # 参数限定
        self.limit = tk.StringVar()
        self.limit.set('0.0')
        self.windLabel = tk.Label(self.root, text="风速限制\n（单位：m/s）")
        self.windText = tk.Entry(self.root, textvariable=self.limit)
        self.isGreater = tk.IntVar()  # IntVar() 用于处理整数类型的变量
        self.isGreater.set(0)  # 根据单选按钮的 value 值来选择相应的选项
        # 使用 variable 参数来关联 IntVar() 的变量 v
        self.lessButton = tk.Radiobutton(self.root, text="小于等于", variable=self.isGreater, value=0)
        self.greaterButton = tk.Radiobutton(self.root, text="大于", variable=self.isGreater, value=1)

        self.filterButton = tk.Button(self.root, text="开始筛选", command=self._filter)

        self.x_limit = tk.StringVar()
        self.x_limit.set(
            '[79.5, 82], [82.5, 85], [85.5, 88], [147., 149.5], [150., 152.5], [153., 155.5], [214.5, 217], '
            '[217.5, 220],[220.5, 223], [282., 284.5], [285., 287.5], [288., 290.5]')
        self.y_limit = tk.StringVar()
        self.y_limit.set(
            '[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], '
            '[15.5, 17.],[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.]')
        self.x_limitLabel = tk.Label(self.root, text="排烟道x方向位置\n（单位：m）")
        self.x_limitText = tk.Entry(self.root, textvariable=self.x_limit)
        self.y_limitLabel = tk.Label(self.root, text="排烟道y方向位置\n（单位：m）")
        self.y_limitText = tk.Entry(self.root, textvariable=self.y_limit)
        self.windLabel.grid(row=2, column=0)
        self.windText.grid(row=2, column=1)
        self.lessButton.grid(row=2, column=2)
        self.greaterButton.grid(row=2, column=3)
        self.x_limitLabel.grid(row=3, column=0)
        self.x_limitText.grid(row=3, column=1)
        self.y_limitLabel.grid(row=4, column=0)
        self.y_limitText.grid(row=4, column=1)
        self.filterButton.grid(row=3, column=2)
        self.root.mainloop()

    def _select_path(self):
        '''
        选择目录路径
        '''
        path_ = tkfile.askdirectory()  # 使用askdirectory()方法返回文件夹的路径
        if path_ == "":
            self.path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            path_ = path_.replace("\\", "/")  # 实际在代码中执行的路径为“\“ 所以替换一下
            self.path.set(path_)

    def _filter(self):
        '''
        执行筛选操作
        '''
        path = self.path.get()
        limit = float(self.limit.get())
        x_limit = self._str2float(self.x_limit.get())
        y_limit = self._str2float(self.y_limit.get())
        isGreater = self.isGreater.get()
        print(path)

        filter_file_path(path, x_limit, y_limit, limit, isGreater)

    def _str2float(self, str):
        '''
        将字符串转换为浮点数列表
        :param str: 文本框输入的字符串
        :return: 浮点数列表
        '''
        str = str.strip(']')
        str = str.split('],')
        ls = []
        for st in str:
            temp = st.split('[')
            s = temp[1].split(',')
            ls.append(list(map(float, s)))
        return ls


mywindow = MyWindow()
