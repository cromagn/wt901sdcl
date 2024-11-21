import os

# 定义桌面路径和文件路径

import threading

tempBuffer = []
filepath = ""
data = []
line = ""
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
filepath = os.path.join('E:', 'WIT00011.TXT')   #Change the file name here

def read_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(102400)
                if not chunk:
                    print("Reading file completed")
                    break
                # print(chunk.decode('utf-8', errors='ignore'))
                processData(chunk)
    except FileNotFoundError:
        print("File not found: ", filepath)
    except Exception as e:
        print("An error occurred:", e)


def write_lines_to_file(filename, lines):
    global data
    try:
        with open(filename, 'a') as f:
            for line in lines:
                f.write(line + '\n')
            data.clear()
    except Exception as e:
        print("An error occurred:", e)


def processData(chunk):
    global tempBuffer
    global data
    tempdata = bytes.fromhex(chunk.hex())
    for val in tempdata:
        tempBuffer.append(val)
        if tempBuffer[0] != 0x55:
            del tempBuffer[0]
        if len(tempBuffer) == 2:
            if (tempBuffer[1] & 0xf0) != 0x50:
                del tempBuffer[0]
        if len(tempBuffer) >= 11:
            processPack(tempBuffer[:11])
            del tempBuffer[:11]
    # 写入文件
    write_lines_to_file(new_filepath, data)
    pass


def processPack(pack):
    global data
    global line
    if pack[1] == 0x50:
        if line != "":
            data.append(line)
            line = ""
        # time
        year = "20" + str(pack[2])
        mon = pack[3]
        day = pack[4]
        hour = pack[5]
        mins = pack[6]
        second = pack[7]
        mills = pack[9] << 8 | pack[8]
        if mills < 100:
            print(mills)
            print("{:03d}".format(mills))
        line += "{}-{}-{} {}:{}:{:02d}.{:03d}\t".format(year, mon, day, hour, mins, second, mills)
        pass
    elif pack[1] == 0x51:
        # Acc
        Ax = getSignInt16(pack[3] << 8 | pack[2]) / 32768 * 16
        Ay = getSignInt16(pack[5] << 8 | pack[4]) / 32768 * 16
        Az = getSignInt16(pack[7] << 8 | pack[6]) / 32768 * 16
        line += str(round(Ax, 3)) + "\t" + str(round(Ay, 3)) + "\t" + str(round(Az, 3)) + "\t"
    elif pack[1] == 0x52:
        Gx = getSignInt16(pack[3] << 8 | pack[2]) / 32768 * 2000
        Gy = getSignInt16(pack[5] << 8 | pack[4]) / 32768 * 2000
        Gz = getSignInt16(pack[7] << 8 | pack[6]) / 32768 * 2000
        line += str(round(Gx, 3)) + "\t" + str(round(Gy, 3)) + "\t" + str(round(Gz, 3)) + "\t"
    elif pack[1] == 0x53:
        Angx = getSignInt16(pack[3] << 8 | pack[2]) / 32768 * 180
        Angy = getSignInt16(pack[5] << 8 | pack[4]) / 32768 * 180
        Angz = getSignInt16(pack[7] << 8 | pack[6]) / 32768 * 180
        line += str(round(Angx, 3)) + "\t" + str(round(Angy, 3)) + "\t" + str(round(Angz, 3)) + "\t"
    elif pack[1] == 0x54:
        Hx = getSignInt16(pack[3] << 8 | pack[2]) / 120
        Hy = getSignInt16(pack[5] << 8 | pack[4]) / 120
        Hz = getSignInt16(pack[7] << 8 | pack[6]) / 120
        line += str(round(Hx, 3)) + "\t" + str(round(Hy, 3)) + "\t" + str(round(Hz, 3))


def getSignInt16(num):
    if num >= pow(2, 15):
        num -= pow(2, 16)
    return num


if __name__ == "__main__":
    while True:
        #filepath = input("Enter the path to the file: ")

        print("Transferring files, please wait......")

        # 将文件路径分割成各个组成部分
        components = filepath.split('.')
        # 替换倒数第二个组成部分为新的目录名称
        components[-2] = components[-2] + "_new"
        components[-1] = "txt"
        # 将组成部分重新连接起来
        new_filepath = '.'.join(components)

        lines = ["Time\tAccX\tAccY\tAccZ\tAsX\tAsY\tAsZ\tAngX\tAngY\tAngZ\tHX\tHY\tHZ"]
        write_lines_to_file(new_filepath, lines)

        thread = threading.Thread(target=read_file, args=(filepath,))
        thread.start()
        thread.join()

        print("File output:  " + new_filepath)

        user_input = input("Please enter 1 to repeat execution and 2 to exit the script:")

        # 判断用户输入
        if user_input == "1":
            # 用户输入1，继续循环执行脚本
            continue
        elif user_input == "2":
            # 用户输入2，退出循环和脚本
            break
        else:
            # 用户输入非法，提示用户重新输入
            print("Invalid input, please re-enter!")