import numpy as np
def readmala2(file):
    # Read .rad file
    temp_value = None
    header_file = file + '.rad'
    with open(header_file, 'r') as f:
        head_lines = f.readlines()

    header = {}
    for line in head_lines:
        separator_location = line.find(':')
        temp_field = line[:separator_location].strip().replace(' ', '_')
        temp_value_str = line[separator_location + 1:].strip()  # 获取字符串值并去除首尾的空格
        header[temp_field] = temp_value
        if temp_value_str != '':
            temp_value = float(temp_value_str)
            header[temp_field] = temp_value
        else:
            header[temp_field] = None  # 如果字符串为空，则将对应的值设为 None

    # Read .rd3 file
    data_file = file + '.RD3'
    with open(data_file, 'rb') as f:
        data = np.fromfile(f, dtype=np.int16)

    data = data.reshape((-1,int(header['SAMPLES']))).astype(np.int16)

    return header, data