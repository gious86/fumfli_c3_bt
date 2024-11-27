import bluetooth
from micropython import const
import time


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)


class btr:
    def __init__(self, uuid):
        self.id = bytes.fromhex(uuid) 
        self.key = 0
        self.lastt = time.ticks_ms()
        self.bt = bluetooth.BLE()
        
    def bt_irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, connectable, rssi, adv_data = data
            if rssi > -75 and time.ticks_diff(time.ticks_ms(), self.lastt)>5000: #rssi > -75 and
                d = bytes(adv_data)  #4:
                i=d[2:18]
                if i==self.id:
                    self.key = int.from_bytes(d[18:])
                    self.lastt = time.ticks_ms()              
        elif event == _IRQ_SCAN_DONE:
            #self.bt_scan()
            #print('scan complete')
            pass
        
    def scan(self):
        self.bt.irq(self.bt_irq)
        self.bt.active(True)
        self.bt.gap_scan(0, 30000, 30000)
        
    def stop_scan(self):
        self.bt.gap_scan(None)
    
    