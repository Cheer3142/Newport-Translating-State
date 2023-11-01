import usb.core
import usb.util

dev = usb.core.find(find_all=True)
for i in dev:
    try:
        if i.idVendor == 4173:
            break
        print(i.get_active_configuration())
        print(i.idVendor, ">> Active")   
    except:
        print(i.idVendor, ">> Not active")
        
'''
  idVendor: 4173 (0x104d)
  idProduct: 12289 (0x3001)
'''

cfg     = i.get_active_configuration()
intf    = cfg[(0,0)]
ep      = cfg[(0,0)][0]

'''
i.read(ep.bEndpointAddress, size_of_buffer = ep.wMaxPacketSize)
i.write(ep.bEndpointAddress, data = 'test', timeout = 100)
'''
