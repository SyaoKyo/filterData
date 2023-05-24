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
        self.pathText = tk.Entry(self.root, textvariable=self.path, state="readonly", width=60)
        self.pathText.grid(row=0, column=1, columnspan=3)
        self.selectPathButton = tk.Button(self.root, text="选择路径", command=self._select_path)
        self.selectPathButton.grid(row=0, column=4)

        # 参数限定
        self.limit = tk.StringVar()
        self.limit.set('0.0')
        self.windLabel = tk.Label(self.root, text="判定标准\n（单位：m/s）")
        self.windText = tk.Entry(self.root, textvariable=self.limit)
        self.isGreater = tk.IntVar()  # IntVar() 用于处理整数类型的变量
        self.isGreater.set(0)  # 根据单选按钮的 value 值来选择相应的选项
        # 使用 variable 参数来关联 IntVar() 的变量 v

        self.lesserButton = tk.Radiobutton(self.root, text="小于\n（任一方向）", variable=self.isGreater, value=-1)
        self.lesserEqualButton = tk.Radiobutton(self.root, text="小于等于\n（任一方向）", variable=self.isGreater, value=0)
        self.greaterButton = tk.Radiobutton(self.root, text="大于\n（所有方向）", variable=self.isGreater, value=1)

        self.filterButton = tk.Button(self.root, text="开始筛选", command=self._filter)

        self.flue_x_limit = tk.StringVar()
        self.flue_x_limit.set(
            '[79.5, 82], [82.5, 85], [85.5, 88], [147., 149.5], [150., 152.5], [153., 155.5], [214.5, 217], '
            '[217.5, 220],[220.5, 223], [282., 284.5], [285., 287.5], [288., 290.5]')
        self.flue_y_limit = tk.StringVar()
        self.flue_y_limit.set(
            '[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], '
            '[15.5, 17.],[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.]')
        self.flue_z_limit = tk.StringVar()
        self.flue_z_limit.set(
            '[3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], '
            '[3.6, 7.2],[3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2]')
        self.vent_x_limit = tk.StringVar()
        self.vent_x_limit.set(
            '[79.5, 82], [82.5, 85], [85.5, 88], [147., 149.5], [150., 152.5], [153., 155.5], [214.5, 217], '
            '[217.5, 220],[220.5, 223], [282., 284.5], [285., 287.5], [288., 290.5]')
        self.vent_y_limit = tk.StringVar()
        self.vent_y_limit.set(
            '[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.], '
            '[15.5, 17.],[15.5, 17.], [15.5, 17.], [15.5, 17.], [15.5, 17.]')
        self.vent_z_limit = tk.StringVar()
        self.vent_z_limit.set(
            '[3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2], '
            '[3.6, 7.2],[3.6, 7.2], [3.6, 7.2], [3.6, 7.2], [3.6, 7.2]')

        self.flue_x_limitLabel = tk.Label(self.root, text="排烟道x方向位置\n（单位：m）")
        self.flue_x_limitText = tk.Entry(self.root, textvariable=self.flue_x_limit)
        self.flue_y_limitLabel = tk.Label(self.root, text="排烟道y方向位置\n（单位：m）")
        self.flue_y_limitText = tk.Entry(self.root, textvariable=self.flue_y_limit)
        self.flue_z_limitLabel = tk.Label(self.root, text="排烟道z方向位置\n（单位：m）")
        self.flue_z_limitText = tk.Entry(self.root, textvariable=self.flue_z_limit)
        self.vent_x_limitLabel = tk.Label(self.root, text="排烟口x方向位置\n（单位：m）")
        self.vent_x_limitText = tk.Entry(self.root, textvariable=self.vent_x_limit)
        self.vent_y_limitLabel = tk.Label(self.root, text="排烟口y方向位置\n（单位：m）")
        self.vent_y_limitText = tk.Entry(self.root, textvariable=self.vent_y_limit)
        self.vent_z_limitLabel = tk.Label(self.root, text="排烟口z方向位置\n（单位：m）")
        self.vent_z_limitText = tk.Entry(self.root, textvariable=self.vent_z_limit)

        self.windLabel.grid(row=2, column=0)
        self.windText.grid(row=2, column=1)
        self.lesserButton.grid(row=2, column=2)
        self.lesserEqualButton.grid(row=2, column=3)
        self.greaterButton.grid(row=2, column=4)
        self.flue_x_limitLabel.grid(row=3, column=0)
        self.flue_x_limitText.grid(row=3, column=1)
        self.flue_y_limitLabel.grid(row=4, column=0)
        self.flue_y_limitText.grid(row=4, column=1)
        self.flue_z_limitLabel.grid(row=5, column=0)
        self.flue_z_limitText.grid(row=5, column=1)
        self.vent_x_limitLabel.grid(row=3, column=2)
        self.vent_x_limitText.grid(row=3, column=3)
        self.vent_y_limitLabel.grid(row=4, column=2)
        self.vent_y_limitText.grid(row=4, column=3)
        self.vent_z_limitLabel.grid(row=5, column=2)
        self.vent_z_limitText.grid(row=5, column=3)
        self.filterButton.grid(row=3, column=4)
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

        # 排烟道xyz限制
        flue_x_limit = self._str2float(self.flue_x_limit.get())
        flue_y_limit = self._str2float(self.flue_y_limit.get())
        flue_z_limit = self._str2float(self.flue_z_limit.get())

        # 排烟口xyz限制
        vent_x_limit = self._str2float(self.vent_x_limit.get())
        vent_y_limit = self._str2float(self.vent_y_limit.get())
        vent_z_limit = self._str2float(self.vent_z_limit.get())

        # 判定方式
        isGreater = self.isGreater.get()
        print(path)

        filter_file_path(path, flue_x_limit, flue_y_limit, flue_z_limit, vent_x_limit, vent_y_limit, vent_z_limit,
                         limit, isGreater)

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
