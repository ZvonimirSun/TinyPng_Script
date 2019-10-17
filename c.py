import os
import time
import json
import tinify

if os.path.isfile('./config.json'):
    pass
else:
    print("配置文件 config.json 不存在。")
    os._exit(0)

with open('./config.json', 'r') as f:
    temp = json.loads(f.read())
    keys = temp["keys"]
    fromPath = temp["fromPath"]  # source path
    toPath = temp["toPath"]  # dest path
    ignorePath = temp["ignorePath"]
    ignoreFile = temp["ignoreFile"]

count = 0

print('开始处理图片文件。')
print('\n参数信息:')
print('\t源文件夹为 ' + fromPath)
print('\t目标文件夹为 ' + toPath)
startTime = time.time()

for root, dirs, files in os.walk(fromPath):
    newToPath = toPath
    newFromPath = fromPath
    if len(root) > len(fromPath):
        innerPath = root[len(fromPath):]
        if innerPath[0] == '/':
            innerPath = innerPath[1:]
        newToPath = os.path.join(toPath, innerPath)
        newFromPath = os.path.join(fromPath, innerPath)

    for name in files:
        newFromFilePath = os.path.join(root, name)
        if all(path not in newFromFilePath for path in ignorePath):
            if (newFromFilePath not in ignoreFile):
                newToFilePath = os.path.join(newToPath, name)
                fileName, fileSuffix = os.path.splitext(name)
                if fileSuffix == '.png' or fileSuffix == '.jpg':
                    tinify.key = keys[count % len(keys)]
                    count += 1
                    print('\n正在处理第' + str(count) + '个图片。')
                    if os.path.exists(newToFilePath):
                        print('图片已压缩过，跳过。')
                    else:
                        source = tinify.from_file(newFromFilePath)
                        source.to_file(newToFilePath)
                        print('图片压缩完成。')
                else:
                    print('\n非图片文件，已跳过。')
            else:
                print('\n文件被忽略，已跳过。')

    for dirName in dirs:
        if all(path not in os.path.join(newFromPath, dirName)
               for path in ignorePath):
            if not os.path.exists(os.path.join(newToPath, dirName)):
                os.mkdir(os.path.join(newToPath, dirName))
        else:
            print('\n文件夹' + os.path.join(newFromPath, dirName) + '被忽略，已跳过。')

endTime = time.time()
print('\n总用时: ' + str(round(endTime - startTime, 2)) + '秒')
os._exit(0)
