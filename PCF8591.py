# 模拟输入不能超过3.3V
import smbus
import time

bus = smbus.SMBus(1)


def setup(Addr):
    global address
    address = Addr


def read(chn):  # 通道选择 0~3之间
    try:
        if chn == 0:
            bus.write_byte(address, 0x40)  # 0100 0000
        if chn == 1:
            bus.write_byte(address, 0x41)  # 0100 0001
        if chn == 2:
            bus.write_byte(address, 0x42)  # 0100 0010
        if chn == 3:
            bus.write_byte(address, 0x43)  # 0100 0011
        bus.read_byte(address)  # 开始读写转换
    except Exception as e:
        print("Address :%s" % address)
        print(e)
    return bus.read_byte(address)

# 模块模拟输出量控制，范围为0~255
def write(val):
    try:
        temp = val  # 将数值赋给temp变量
        temp = int(temp) # 将字符串转换为整型
        # 在终端上打印temp以查看，否则将注释掉
        bus.write_byte_data(address, 0x40, temp)
    except Exception as e:
        print("Error: Device address: 0x%2X" % address)
        print(e)


if __name__ == '__main__':
    setup(0x48)
    while True:
        print("AIN0 = ", read(0))
        print("AIN1 = ", read(1))
        tmp = read(0)
        tmp = tmp * (255 - 125) / 255 + 125
        # 低于125时LED不会亮，所以转换
        write(tmp)
        # time.sleep(0.3)
