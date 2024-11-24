import os

import threading

tempBuffer = []
data = []
line = ""
filepath = os.path.join('E:', 'WIT00011.TXT')   # Change the file name here


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
        line += "{}-{}-{} {}:{:02d}:{:02d}.{:03d}\t".format(year, mon, day, hour, mins, second, mills)
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

    print("Reading file, please wait......")
    components = filepath.split('.')
    components[-2] = components[-2] + "_new"
    components[-1] = "txt"
    new_filepath = '.'.join(components)
    lines = ["Time\tAccX\tAccY\tAccZ\tAsX\tAsY\tAsZ\tAngX\tAngY\tAngZ\tHX\tHY\tHZ"]
    write_lines_to_file(new_filepath, lines)
    thread = threading.Thread(target=read_file, args=(filepath,))
    thread.start()
    thread.join()

    print("File output:  " + new_filepath)
