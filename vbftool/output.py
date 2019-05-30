def writeline(fp, s):
    fp.write(b'%s\r\n' % s.encode('utf-8'))


def newline(fp):
    fp.write(b'\r\n')
