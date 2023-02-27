from PythonSDK.DBDynamics import Ant
import time
import serial
# import serial.tools.list_ports


class DBD_RUN_XY:
    def __init__(self):
        # portName = ''
        # port_list = list(serial.tools.list_ports.comports())
        # com_list = []
        # for i, com in enumerate(port_list):
        #     if "USB-SERIAL" in com.description:
        #         portName = com.device
        #         com_list.append(i)
        #         break
        # self.DBD = Ant(portName)
        self.DBD = Ant("COM4")
        # self.ID = self.DBD.scanDevices()[0] if len(self.DBD.scanDevices()) == 0 else 1
        self.ID = 1
        self.DBD.setPositionMode(self.ID)
        self.DBD.setPowerOn(self.ID)
        # self.DBD.setRunningCurrent(self.ID, 500)
        # self.DBD.setKeepingCurrent(self.ID, 300)
        self.DBD.setTargetVelocity(self.ID, 500)
        self.DBD.setAccTime(self.ID, 100)
        # print(self.DBD.getActualVelocity(self.ID))
        # 默认找零点
        self.set_zero()

    def forward_90(self):  # 母鸡
        self.DBD.setTargetPosition(self.ID, -12500)  # 90°
        self.DBD.waitTargetPositionReached(self.ID)
        self.DBD.setTargetPosition(self.ID, 0)
        self.DBD.waitTargetPositionReached(self.ID)

    def backward_90(self):  # 公鸡
        self.DBD.setTargetPosition(self.ID, 12500)  # 90°
        self.DBD.waitTargetPositionReached(self.ID)
        self.DBD.setTargetPosition(self.ID, 0)
        self.DBD.waitTargetPositionReached(self.ID)

    def forward(self, step=1):
        self.DBD.setTargetPosition(self.ID, 50000 * step)
        self.DBD.waitTargetPositionReached(self.ID)

    def backward(self, step=1):
        self.DBD.setTargetPosition(self.ID, -50000 * step)
        self.DBD.waitTargetPositionReached(self.ID)

    def set_zero(self):
        self.DBD.setHomingDirection(self.ID, 1)
        self.DBD.setTargetVelocity(self.ID, 200)
        self.DBD.setHomingLevel(self.ID, 0)
        self.DBD.setHomingMode(self.ID)
        # self.DBD
        self.DBD.waitTargetPositionReached(self.ID)

    def stop(self):
        self.DBD.stop()


if __name__ == '__main__':
    run = DBD_RUN_XY()
    time.sleep(1)
    # run.forward(30)#15
    run.backward(55)
    # run.backward(0)
    # run.forward(33)
    # run.forward(0)  
    # run.backward_90()
    # run.forward_90()
    run.stop()
