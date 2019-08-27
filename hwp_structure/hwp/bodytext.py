
from zlib import decompress

def Decompress(in_buffer):
    return decompress(in_buffer, -15)

def DecompressFile(file_name):
    in_buffer = file('/home/forest/fuzzer/hwp/test.hwp', "rb").read()
    out_buffer = Decompress(in_buffer)
    
    name = file_name.split(".")[0]
    ext = file_name.split(".")[1]
    out_name = "%s_dec%s" % (name, ext)
    file(out_name, "wb").write(out_buffer)
    return out_name

def GetTag(val):
    RECORD_MEMBER_NAME = ["TagID", "Level", "Size"]
    RECORD_MEMBER_OFFSET = [0, 10, 20]
    RECORD_MEMBER_SIZE = [10, 10, 12]
    return bitMap(val, RECORD_MEMBER_NAME, RECORD_MEMBER_OFFSET, RECORD_MEMBER_SIZE)
    
def GetTagObject(data, offset):
    val = unpack("<L", data[offset:offset+4])[0]
    offset += 4
    tag = GetTag(val)
    
    if tag.Size >= 4095:
        new_size = unpack("<L", data[offset:offset+4])[0]
        offset += 4
        tag = tag._replace(**{"Size":new_size})
        
    tmp = data[offset:offset+tag.Size]
    offset += tag.Size
    
    data = namedtuple("TagData", "data")(tmp)
    
    return namedtuple("Record", tag._fields + data._fields)(*(tag + data)), offset
    
        
def GetRecord(file_name):
    data = file(file_name, "rb").read()
    
    offset = 0
    while offset < len(data):
        print "[0x%08X]" % offset,
        taginfo, offset = GetTagObject(data, offset)
        print taginfo.TagID, taginfo.Level, hex(taginfo.Size)
    return "OK"
    
section0 = r"Section0.dmp"
section0_dec = DecompressFile(section0)
print GetRecord(section0_dec)
