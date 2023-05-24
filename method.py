import pandas as pd
import numpy as np
import os


def filter_file_path(path, flue_x_limit, flue_y_limit, flue_z_limit, vent_x_limit, vent_y_limit, vent_z_limit, limit,
                     isGreater):
    '''
    寻找文件目录下原始数据文件并进行数据筛选
    :param path: 文件目录路径
    :param flue_x_limit: 排烟道x方向限制
    :param flue_y_limit: 排烟道y方向限制
    :param flue_z_limit: 排烟道z方向限制
    :param vent_x_limit: 排烟口x方向限制
    :param vent_y_limit: 排烟口y方向限制
    :param vent_z_limit: 排烟口z方向限制
    :param limit: 风速限制
    :param isGreater: 判定条件
    '''
    fileList = os.listdir(path)
    flueList = []  # 排烟道文件列表
    ventList = []  # 排烟口文件列表
    # 寻找文件目录下原始数据文件
    for fileName in fileList:
        if fileName.find('v2') != -1:
            flueList.append(os.path.join(path, fileName).replace("\\", "/"))
        elif fileName.find('v3') != -1:
            ventList.append(os.path.join(path, fileName).replace("\\", "/"))
        else:
            continue

    # 文件名排序
    ventList.sort(key=len)

    # 数据筛选
    filter_flue_data(flueList, flue_x_limit, flue_y_limit, flue_z_limit, limit, isGreater)
    filter_vent_data(ventList, vent_x_limit, vent_y_limit, vent_z_limit, limit, isGreater)


def filter_flue_data(fileList, x_limit, y_limit, z_limit, limit, isGreater):
    '''
    排烟道数据筛选
    :param fileList: 文件目录列表
    :param x_limit: 排烟道x方向限制
    :param y_limit: 排烟道y方向限制
    :param z_limit: 排烟道z方向限制
    :param limit: 风速限制
    :param isGreater: 判定条件
    '''
    for fileName in fileList:
        filePath = os.path.dirname(fileName)
        # 判断风速限制
        if isGreater > 0:
            writer = pd.ExcelWriter(
                '{}排烟道大于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]).replace("\\", "/"), limit))
        elif isGreater < 0:
            writer = pd.ExcelWriter(
                '{}排烟道小于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]).replace("\\", "/"), limit))
        else:
            writer = pd.ExcelWriter(
                '{}排烟道小于等于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]).replace("\\", "/"), limit))
        # 读取排烟道数据
        df = pd.read_csv('{}'.format(fileName))[1:]
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
        df = df.to_numpy()
        partFilterList = []
        partSumList = []
        for i in range(len(x_limit)):
            # 限制Z
            a = df[df[:, 2] <= z_limit[i][1]]
            a = a[z_limit[i][0] <= a[:, 2]]

            # 限制Y
            a = a[a[:, 1] <= y_limit[i][1]]
            a = a[y_limit[i][0] <= a[:, 1]]

            # 限制X
            b = a[a[:, 0] <= x_limit[i][1]]
            b = b[x_limit[i][0] <= b[:, 0]]

            # 限制U、V
            if isGreater > 0:
                # U、V均大于limit
                c = b[b[:, 3] > limit]
                c = c[c[:, 4] > limit]
            elif isGreater < 0:
                # U或V小于limit
                c1 = b[b[:, 3] < limit]
                c2 = b[b[:, 4] < limit]
                c = np.vstack((c1, c2))
            else:
                # U或V小于等于limit
                c1 = b[b[:, 3] <= limit]
                c2 = b[b[:, 4] <= limit]
                c = np.vstack((c1, c2))

            # 去重
            if c.shape[0] > 0:
                c = np.array(list(set([tuple(t) for t in c])))

            # 存档
            result = np.array(c)
            result = pd.DataFrame(result)
            result.to_excel(writer, sheet_name='{}-{}'.format(x_limit[i][0], x_limit[i][1]),
                            header=['X', 'Y', 'Z', 'U', 'V', 'W'], index=None)

            partFilterList.append(c.shape[0])
            partSumList.append(b.shape[0])
        partFilterList = np.array(partFilterList)
        partSumList = np.array(partSumList)
        sumInfo = np.vstack((partFilterList, partSumList))
        sumInfo = pd.DataFrame(sumInfo)
        sumInfo.index = ['匹配点数', '总点数']
        sumInfo.to_excel(writer, sheet_name='总体统计', header=[_ + 1 for _ in range(len(x_limit))])
        writer.save()


def filter_vent_data(fileList, x_limit, y_limit, z_limit, limit, isGreater):
    '''
    排烟口数据筛选
    :param fileList: 文件目录列表
    :param x_limit: 排烟口x方向限制
    :param y_limit: 排烟口y方向限制
    :param z_limit: 排烟口z方向限制
    :param limit: 风速限制
    :param isGreater: 判定条件
    :return:
    '''
    partLeftFilterList = []
    partRightFilterList = []
    partLeftandRightFilterList = []
    partSumList = []
    filePath = os.path.dirname(fileList[0])
    NameList = [name.split('/')[-1] for name in fileList]
    if isGreater > 0:
        writer1 = pd.ExcelWriter('{}排烟口大于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
        writer2 = pd.ExcelWriter('{}排烟口大于{}-区分左右侧.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
    elif isGreater < 0:
        writer1 = pd.ExcelWriter('{}排烟口小于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
        writer2 = pd.ExcelWriter('{}排烟口小于{}-区分左右侧.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
    else:
        writer1 = pd.ExcelWriter(
            '{}排烟口小于等于{}.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
        writer2 = pd.ExcelWriter(
            '{}排烟口小于等于{}-区分左右侧.xlsx'.format(os.path.join(filePath, filePath.split('/')[-1]), limit))
    for i, fileName in enumerate(fileList):

        # 读取排烟口数据
        df = pd.read_csv('{}'.format(fileName))[1:]
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
        df = df.to_numpy()
        print(fileName, x_limit[i], y_limit[i], z_limit[i])
        # 限制Z
        a = df[df[:, 2] <= z_limit[i][1]]
        a = a[z_limit[i][0] <= a[:, 2]]
        # print('Z',a)
        # 限制Y
        a = a[a[:, 1] <= y_limit[i][1]]
        a = a[y_limit[i][0] <= a[:, 1]]
        # print('Y',a)
        # 限制X
        b = a[a[:, 0] <= x_limit[i][1]]
        b = b[x_limit[i][0] <= b[:, 0]]
        # print('X',b)
        # 限制U、V
        if isGreater > 0:
            # U、V均大于limit
            c = b[b[:, 3] > limit]
            c = c[c[:, 4] > limit]
        elif isGreater < 0:
            # U或V小于limit
            c1 = b[b[:, 3] < limit]
            c2 = b[b[:, 4] < limit]
            c = np.vstack((c1, c2))
        else:
            # U或V小于等于limit
            c1 = b[b[:, 3] <= limit]
            c2 = b[b[:, 4] <= limit]
            c = np.vstack((c1, c2))

        # 去重
        if c.shape[0] > 0:
            c = np.array(list(set([tuple(t) for t in c])))

        # 划分区域
        c0 = c[np.argsort(c[:, 0])]
        split_value = (c0[-1, 0] + c0[0, 0]) / 2
        c1 = c0[c0[:, 0] <= split_value]
        c1 = c1[np.argsort(c1[:, 1])]
        c2 = c0[c0[:, 0] > split_value]
        c2 = c2[np.argsort(c2[:, 1])]

        result1 = np.array(c1)
        result2 = np.array(c2)
        result3 = np.array(c)
        result1 = pd.DataFrame(result1)
        result2 = pd.DataFrame(result2)
        result3 = pd.DataFrame(result3)
        # print(fileName)
        result1.to_excel(writer2, sheet_name='{}左'.format(fileName.split('/')[-1]),
                         header=['X', 'Y', 'Z', 'U', 'V', 'W'], index=None)
        result2.to_excel(writer2, sheet_name='{}右'.format(fileName.split('/')[-1]),
                         header=['X', 'Y', 'Z', 'U', 'V', 'W'], index=None)
        result3.to_excel(writer1, sheet_name='{}总'.format(fileName.split('/')[-1]),
                         header=['X', 'Y', 'Z', 'U', 'V', 'W'], index=None)
        partLeftFilterList.append(c1.shape[0])
        partRightFilterList.append(c2.shape[0])
        partLeftandRightFilterList.append(c.shape[0])
        partSumList.append(df.shape[0] / 2)
    partLeftFilterList = np.array(partLeftFilterList)
    partRightFilterList = np.array(partRightFilterList)
    partLeftandRightFilterList = np.array(partLeftandRightFilterList)
    partSumList = np.array(partSumList)
    sumLeftInfo = np.vstack((partLeftFilterList, partSumList))
    sumLeftInfo = pd.DataFrame(sumLeftInfo)
    sumLeftInfo.index = ['匹配点数', '总点数']
    sumLeftInfo.to_excel(writer2, sheet_name='左侧总体统计', header=NameList)
    sumRightInfo = np.vstack((partRightFilterList, partSumList))
    sumRightInfo = pd.DataFrame(sumRightInfo)
    sumRightInfo.index = ['匹配点数', '总点数']
    sumRightInfo.to_excel(writer2, sheet_name='右侧总体统计', header=NameList)
    sumLeftandRightInfo = np.vstack((partLeftandRightFilterList, 2 * partSumList))
    sumLeftandRightInfo = pd.DataFrame(sumLeftandRightInfo)
    sumLeftandRightInfo.index = ['匹配点数', '总点数']
    sumLeftandRightInfo.to_excel(writer1, sheet_name='总体统计', header=NameList)
    writer1.save()
    writer2.save()
