# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Turning "*.out" files into "*.csv"
# ------------------------------------------------------------------------------
#
#  本程序可用于将 PsCad 仿真产生的数据转换成 csv 文件，从而更好地与 Matlab、Python 等进行交互
#  具体使用方法，参照：
#  访问以下地址检查是否为最新：
#
#     VicoZhang, 中国广州
# ------------------------------------------------------------------------------
#
#  This Python script is a useful tool which can help you handle the out files
#  produced by your simulation programmers. You can turn the out file into csv,
#  for better use in Matlab, Python and else.
#
#  More information, visit: 
#  Check the latest version:
#
#     VicoZhang, Canton, CHINA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import argparse
from mhrc.automation.utilities.file import File, OutFile
from pathlib import Path


def find_basename(path, ini_basename):  # 获取 basename 的准确形式
    file_list = list(path.glob('*.inf'))  # generator 无法用 in 函数，只能退而求其次
    if path / (ini_basename + '.inf') in file_list:
        return ini_basename  # 说明没有使用 multirun 功能
    elif path / (ini_basename + '_r00001.inf') in file_list:
        return [item.stem.replace('.inf', '') for item in file_list]  # 使用了multirun 功能
    else:
        print('Basename 解析出错，请检查')
        exit()


def turn_csv(bn, source, target):
    if type(bn) is str:
        OutFile(str(source.joinpath(bn))).toCSV()  # 生成 csv 文件
        File.move_files(source, target, '.csv')  # 将文件复制到指定目录
    elif type(bn) is list:
        for item in bn:
            OutFile(str(source.joinpath(item))).toCSV()
        File.move_files(source, target, '.csv')
    else:
        print('csv文件转换出错，请检查')
        exit()
    print('csv文件已转换至{}'.format(str(target)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Please input the simulation file path, '
                                     'such as D:\\Constant_source_short_circuit.gf42')
    parser.add_argument('-i', '--input', type=str, help='simulation file path.')
    parser.add_argument('-o', '--output', type=str, help='transferred file path.')
    parser.add_argument('-b', '--basename', type=str, help='basename of the simulation')

    args = parser.parse_args()

    args.input = Path(args.input)
    args.output = Path(args.output)

    basename = find_basename(args.input, args.basename)
    turn_csv(basename, args.input, args.output)
