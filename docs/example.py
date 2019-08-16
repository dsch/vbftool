import logging
import bincopy

import vbftool.options as opt
from vbftool import Vbf, VbfVersion

logging.basicConfig(level=logging.DEBUG)

bin = bincopy.BinFile()
bin.add_ihex_file('test.hex')

vbf = Vbf(VbfVersion.VERSION_JLR3_0, 0x1000000, 0x3C0000, bin.as_binary())
vbf.add_option(opt.DataFormatIdentifier(1, 0))

with open('reference.vbf', 'wb') as fp:
    vbf.dump(fp)
