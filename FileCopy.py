# version 2.0

import os
import sys
import shutil

def longest_common_prefix(strs):
    # 如果输入的数组为空，返回空字符串
    if not strs:
        return ""

    # 将数组按字母顺序排序
    strs.sort()

    # 比较第一个字符串和最后一个字符串的字符
    # 因为它们是数组中的最小和最大值，所以它们的公共前缀也是数组中所有字符串的公共前缀
    first_str = strs[0]
    last_str = strs[-1]
    common_prefix = []
    
    for i in range(len(first_str)):
        if i < len(last_str) and first_str[i] == last_str[i]:
            common_prefix.append(first_str[i])
        else:
            break

    return ''.join(common_prefix)


# 获取当前脚本文件的绝对路径
current_script_path = os.path.abspath(__file__)
# 获取当前脚本文件所在的目录
copy_to_path_root = os.path.dirname(current_script_path) + "\\"

# 创建一个空列表来存储输入的数据
data_list = []

# 使用循环读取多行输入，直到用户输入空行为止
while True:
    # 从用户输入中读取一行数据
    line = input("请输入数据路径（留空结束输入）: ")
    
    # 如果用户输入为空行，退出循环
    if not line:
        break
    line = line.replace('/', '\\')
    
    dot_index = line.rfind(".")
    if (dot_index == -1):
        if line.endswith("\\") is False:
            line = line + '\\'

    # 将读取的数据添加到列表中
    data_list.append(line)

# 打印存储的数据
# print("存储的数据:")
# for data in data_list:
#     print(data)

longest_common_prefix_result = longest_common_prefix(data_list)
if longest_common_prefix_result.endswith("\\") is False:
    longest_common_prefix_result = longest_common_prefix_result + "\\"

print("最长公共前缀:\n", longest_common_prefix_result)

root_dirs = ["Engine\\", "Source\\", "Content\\", "Plugins\\", "Config\\"]

last_occurrence = -1

# 遍历 root_dirs，找到第一个出现的 root_dir
for root_dir in root_dirs:
    position = longest_common_prefix_result.find(root_dir)
    if position != -1 :
        last_occurrence = position
        break

# 待检查的目录路径，检查它是否是引擎目录，或者是项目目录
check_path = ""
if (last_occurrence == -1):
# 输入的路径应该都不包含"Engine\"，可能是Game项目路径，也可能既不是Game项目路径也不是引擎的路径
   check_path = longest_common_prefix_result
else:
   check_path = longest_common_prefix_result[0:last_occurrence]


# 检查它是否是引擎目录，或者是项目目录
# 获取目录中的所有文件
files_in_directory = os.listdir(check_path)
# 检查是否存在 .sln 后缀的文件
sln_files = [file for file in files_in_directory if file.endswith('.sln')]
if sln_files:
    # 最长公共前缀就是Game项目的根目录
    last_occurrence = len(check_path)
else:
    exit()


# 你的UE项目路径
ue_proj_path = longest_common_prefix_result[0:last_occurrence]
print("你的UE项目路径:\n", ue_proj_path)

# 复制文件
print("\n开始复制文件:\n")
for sour in data_list:
    # 去掉 UE项目路径
    sour = sour[last_occurrence:]
    i = sour.rfind('\\')

    sour_path = sour[:i+1] # Engine\Content\Editor\Slate\Icons\AssetIcons\
    # print("sour_path: " + sour_path)
    sour_file = sour[i+1:] # AtmosphericFog_64x.png
    # print("sour_file: " + sour_file)

    isDirectory = len(sour_file) == 0 or sour_file == '\\'
    
    outPath = copy_to_path_root + 'OutputFiles\\' + sour_path
    # print("outPath: " + outPath)

    sourceFile = ue_proj_path + sour
    # print("sourceFile: " + sourceFile)
    destinationFile = outPath + sour_file
    # print("destinationFile: " + destinationFile)
    
    # create pre director
    if os.path.exists(outPath) == False:
        os.makedirs(outPath)

    # copy sour file
    if isDirectory == True:
        # 删除已经存在的文件夹
        if os.path.exists(destinationFile):
            shutil.rmtree(destinationFile)
        shutil.copytree(sourceFile, destinationFile)
    else:
        # 删除已经存在的文件
        if os.path.exists(destinationFile):
            os.remove(destinationFile)
        shutil.copy(sourceFile, outPath)

    print("Copy successfully!")

print("复制完成！")
    