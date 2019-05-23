from vbftool.vbf import Vbf
import bincopy

bin = bincopy.BinFile()
bin.add_ihex_file('test.hex')

vbf = Vbf(0x1000000, 0x3C0000, bin.as_binary())

with open('reference.vbf', 'wb') as fp:
    vbf.dump(fp)
