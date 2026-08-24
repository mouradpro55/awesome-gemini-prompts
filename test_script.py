import pycdlib
# creating a dummy iso to test extraction logic
iso = pycdlib.PyCdlib()
iso.new(interchange_level=3)
iso.add_fp(b"dummy content", 13, '/DUMMY.TXT;1')
iso.write('dummy.iso')
iso.close()
