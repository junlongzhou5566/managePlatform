# -*- coding: UTF-8 -*-
'''
Created on Oct 23, 2009

@author: petr
'''
import codecs
from hessian.UTF8 import readSymbol, readString, symbolToUTF8 

# ----------------------------------------------------------
# Attic

def readString2(source, size):
    "This version is far slower than readString that joins list of chars"
    result = u""
    for _ in range(size):
        result += unichr(readSymbol(source.read))
    return result

# ----------------------------------------------------------
# Tests

def bruteDecoderTest():
    from StringIO import StringIO    
    for c in xrange(0, 0xffff):
        assert readSymbol(StringIO(unichr(c).encode("UTF-8")).read) == c
         
def test():    
    from StringIO import StringIO
    src = u"""
    В этом нет ничего нового,
    Ибо вообще ничего нового нет.
        Николай Рерих        
    ÀùúûüýþÿĀāĂăĄąĆćĈĉ
    $¢£¤¥₣₤₧₪₫€
    """    
    #u0 = src.encode("UTF-8")
    u1 = ""
    for c in src:
        u1 += "".join(symbolToUTF8(ord(c)))
    assert u1.decode("UTF-8") == src
    s = []
    s_read = StringIO(u1)
    while True:
        repr = readSymbol(s_read.read)
        if repr == None:
            break
        s.append(unichr(repr))
        
    s = u"".join(s)
    assert s == src

def testExceptions():
    def decodeStr(s):
        from StringIO import StringIO        
        s_read = StringIO(s)
        return readSymbol(s_read.read)
    def expectException(funcall):
        try: 
            funcall()            
        except Exception:
            pass
        else:
            assert False
    expectException(lambda: decodeStr("\xff"))
    expectException(lambda: decodeStr("\x80")) 
    expectException(lambda: decodeStr("\xc0\x00"))
    expectException(lambda: decodeStr("\xe0\x80\x00"))
    

def testPerformance():
    from StringIO import StringIO
    from time import time as now
    src = u"(Цой|punk|Ленин)Жив!" * 20000
    u0 = src.encode("UTF-8")
    #--------------------------
    tStart = now()
    for c in src:
        symbolToUTF8(ord(c))
    tEncode = now() - tStart
    print "Encoding",  (len(src) / tEncode), "symbols/sec"
    #--------------------------
    # Test native encorder
    tStart = now()
    src.encode("UTF-8")    
    tEncode = now() - tStart
    print "Encoding (native)",  (len(src) / tEncode), "symbols/sec"
    #--------------------------
    tStart = now()
    s_read = StringIO(u0)
    while True:
        repr = readSymbol(s_read.read)
        if repr == None:
            break 
    tDecode = now() - tStart       
    print "Decoding",  (len(src) / tDecode), "symbols/sec"    
    #--------------------------
    tStart = now()
    s_read = StringIO(u0)
    readString(s_read, len(src))     
    tDecode = now() - tStart       
    print "Decoding(readString)",  (len(src) / tDecode), "symbols/sec"
    #--------------------------
#    tStart = now()
#    s_read = StringIO(u0)
#    readString2(s_read, len(src))     
#    tDecode = now() - tStart       
#    print "Decoding(readString2)",  (len(src) / tDecode), "symbols/sec"    
    #--------------------------
    # Test native decorders
    reader = codecs.lookup("UTF-8").streamreader(StringIO(u0), 'strict')
    tStart = now()
    chunk = 4096
    while True:        
        # :( If read size is > 1 this may read beyond string and break parser
        # With read size == 1 it is even slower than hand-written procedure (for non ascii chars)
        readSize = 1 
        repr = reader.read(readSize, chunk)
        if len(repr) == 0:
            break 
    tDecode = now() - tStart       
    print "Decoding(native)",  (len(src) / tDecode), "symbols/sec"


if __name__ == "__main__":
    bruteDecoderTest()
    test()
    testExceptions()
    testPerformance()
    print "Tests passed."
