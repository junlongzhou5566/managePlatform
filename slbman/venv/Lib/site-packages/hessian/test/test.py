# -*- coding: UTF-8 -*-
#
# Hessian protocol implementation test
#
# Protocol specification can be found here
# http://hessian.caucho.com/doc/hessian-1.0-spec.xtp
#
# This file contains some tests for HessianPy library.
#
# Copyright 2005 Petr Gladkikh (batyi at users sourceforge net)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from hessian.hessian import ParseContext, WriteContext, readObjectByPrefix
from hessian import hessian  
from hessian.client import HessianProxy
from hessian.server import HessianHTTPRequestHandler, StoppableHTTPServer
from StringIO import StringIO
from time import sleep
from threading import Thread
import traceback


__revision__ = "$Rev: 95 $"


class TestException(Exception):    
    def __init__(self, message):
        self.testMessage = message


def readObjectString(txt):
    stream = StringIO(txt)
    return readObjectByPrefix(ParseContext(stream), stream.read(1))


def parseData(txt):
    """Auxiliary function.
    Takes plain text description of binary data 
    from protocol specification and returns binary data"""
    import re
    result = ""
    for a in re.split('\s+', txt):
        if re.match('x[0-9a-f]{2}', a, re.IGNORECASE):            
            result += chr(int(a[1:], 16))
        else:
            result += a    
    return result


def autoLoopBackTest(value):
    s = StringIO()
    hessian.writeObject(WriteContext(s), value, None)    
    s.seek(0)    
    r = readObjectByPrefix(ParseContext(s), s.read(1))
    assert r == value
        
    
def loopBackTest(classRef, value):
    s = StringIO()
    o = classRef()
    o.write(WriteContext(s), value)
    s.seek(0)
    r = hessian.readObject(ParseContext(s))
    res = False
    try:
        res = r == value
    except RuntimeError:
        # Fall-back in case of recursion error
        res = `r` == `value`        
    assert res


def loopBackTestTyped(classRef, value, converter=None):
    """ This test is for objects with ambiguous type prefixes,
    'converter' is used for types that are not preserved after
    serialization
    """
    s = StringIO()
    o = classRef()
    o.write(WriteContext(s), value)
    s.seek(0)
    s_in = ParseContext(s)
    if converter != None:
        value = converter(value)
    assert o.read(s_in, s_in.read(1)) == value


def loopbackTestTypes():
    loopBackTest(hessian.Null, None)
    loopBackTest(hessian.Bool, True)
    loopBackTest(hessian.Bool, False)    
    loopBackTest(hessian.Int, 12343)
    loopBackTest(hessian.Long, 2403914806071207089L)
    loopBackTest(hessian.Double, 0.0)
    loopBackTest(hessian.Double, 123.321)
    loopBackTest(hessian.UnicodeString, u"")
    loopBackTest(hessian.UnicodeString, u"Nice to see ya! длорфызвабьйтцуикзгшщчсмжячмс.")
    loopBackTest(hessian.UnicodeString, "Wahappan?")
    loopBackTest(hessian.Array, [])
    loopBackTest(hessian.Array, ["123", 1])
    loopBackTest(hessian.Array, [3, 3])
    loopBackTest(hessian.Array, [None, [3]])
    loopBackTest(hessian.Array, [[[3]]])
    loopBackTest(hessian.Map, {})
    loopBackTest(hessian.Map, {1 : 2})
    loopBackTest(hessian.Remote, hessian.RemoteReference("yo://yeshi/yama"))
        
    loopBackTestTyped(hessian.Tuple, (), list)
    loopBackTestTyped(hessian.Tuple, (1,), list)
    loopBackTestTyped(hessian.Tuple, ("equivalence", 1, {"":[]}), list)
    
    autoLoopBackTest(
        u"\x07Nice to see ya! )*)(*РєР°РјРїСѓС‚РµСЂ&)(*\x00&)(*&)(*&&*\x09^%&^%$%^$%$!#@!")
    autoLoopBackTest(
        "\x07Nice to see ya! )*)(*РєР°РјРїСѓС‚РµСЂ&)(*\x00&)(*&)(*&&*\x09^%&^%$%^$%$!#@!")
    autoLoopBackTest(u"Пррревед обонентеги!")


def testDatetime():
    from datetime import datetime 
    loopBackTest(hessian.Date, datetime.fromtimestamp(0))
    loopBackTest(hessian.Date, datetime.fromtimestamp(987654321))
    autoLoopBackTest(datetime.fromtimestamp(3333))
    
    # Test that time precision is at least millisecond
    def wr(val):
        s = StringIO()
        hessian.Date().write(WriteContext(s), datetime.fromtimestamp(val))
        s.seek(0)
        return hessian.readObject(ParseContext(s))    
    
    assert wr(0.001).time().microsecond != wr(0.002).time().microsecond  
    assert wr(1345.999).time().microsecond != wr(1346.0).time().microsecond
    assert wr(12345.0) == wr(12345.0)    

   
def testHessianTypes():
    "Test explicit setting of serialized types"    
    autoLoopBackTest(hessian.XmlString(u"<hello who=\"Небольшой текст тут!\"/>"))    
    

def serializeCallTest():    
    loopBackTest(hessian.Call, ("aaa", [], []))
    loopBackTest(hessian.Call, ("aaa", [], [1]))
    loopBackTest(hessian.Call, ("aaa", [], ["ddd", 1]))
    loopBackTest(hessian.Call, ("aaa", [("type", 1)], []))
    loopBackTest(hessian.Call, ("aaa", [("headerName", "headerValue")], [23]))
    loopBackTest(hessian.Call, ("a", [("headerName", "headerValue"),
                               ("headerName2", "headerValue2")], [23]))
    loopBackTest(hessian.Call, ("aaa", [], \
                        [{"name" : "beaver", "value" : [987654321, 2, 3.0] }]))


def serializeReplyAndFaultTest():    
    loopBackTestTyped(hessian.Reply, ([], True, 1))
    loopBackTestTyped(hessian.Reply, ([], True, {"code" : [1, 2]}))
    loopBackTestTyped(hessian.Reply, ([], False, {}))
    loopBackTestTyped(hessian.Reply, ([], False, {"code" : "value"}))
    
    loopBackTestTyped(hessian.Reply, ([("headerName", "headerValue")], True, 33))
    loopBackTestTyped(hessian.Reply, ([("headerName", "headerValue"),
                               ("headerName2", "headerValue2")], True, 33))
    
    loopBackTestTyped(hessian.Fault, {"message":"an error description", "line":23})


def referenceTest():
    m = {"name" : "beaver", "value" : [987654321, 2, 3.0] }
    loopBackTest(hessian.Call, ("aaa", [], [m, m]))
    a = [1, 2, 3]
    a[2] = a
    loopBackTest(hessian.Call, ("aaa", [], [a]))
    b = [a, 1]
    a[0] = b
    loopBackTest(hessian.Call, ("aaa", [], [b, a]))

    
def deserializeTest():
    txt = """V t x00 x03 int
      l x00 x00 x00 x02
      I x00 x00 x00 x00
      I x00 x00 x00 x01
      z"""      
    assert(readObjectString(parseData(txt)) == [0, 1])
    
    txt = """V 
      l xff xff xff xff
      I x00 x00 x00 x00
      I x00 x00 x00 x01
      I x00 x00 x00 x03
      z"""      
    assert(readObjectString(parseData(txt)) == [0, 1, 3])


# ---------------------------------------------------------
# remote call tests


SECRET_MESSAGE = "Hello from HessianPy!"
TEST_PORT = 7777


def warnConnectionRefused(exception, url):    
    print "\nException:", exception
    # If 'Connection refused' or 'getaddrinfo failed'
    if (hasattr(exception, "args") and exception.args[0] in [11001, 10061]) \
        or(hasattr(exception, "args") and exception.reason[0] in [11001, 10061]):
        print "Warning: Server '" + url + "'is not available. Can not perform a remote call test."
        return True
    else:
        return False


class TestHandler(HessianHTTPRequestHandler):   

    OTHER_PREFIX = "somewhere"
    
    def nothing(self):
        pass
    
    def hello(self):
        return SECRET_MESSAGE
    
    def echo(self, some):
        return some
        
    def askBitchy(self):
        raise TestException("Go away!")
    
    def redirect(self, home_url):
        return hessian.RemoteReference(home_url + TestHandler.OTHER_PREFIX)
    
    def sum(self, a, b):
        return a + b
    
    message_map = {
                   "nothing" : nothing,
                   "hello" : hello,
                   "askBitchy" : askBitchy,
                   "echo" : echo,
                   "redirect" : redirect,
                   "sum" : sum }


class TestServer(Thread):    
    def run(self):
        print "\nStarting test HTTP server"
        server_address = ('localhost', TEST_PORT)
        self.httpd = StoppableHTTPServer(server_address, TestHandler)
        print "Serving from ", server_address
        self.httpd.serve()
        
    def stop(self):
        self.httpd.stop()


def callBlobTest(proxy):    
    size = 2 ** 14
    big = u"ЦЦ*муха" * size
    r = proxy.echo(big)
    assert big == r
    
    
def redirectTest(proxy):
    proxy2 = proxy.redirect(proxy.url)
    s = proxy2.sum(654321, 123456)
    assert s == 777777
    
    p = proxy    
    for _ in range(3): p = p.echo(p)
    assert p.hello() == SECRET_MESSAGE
  

def callTestLocal(url):
    srv = TestServer()
    srv.setDaemon(True)
    srv.start()
    # Due to some reason server does not accept connections right after it's started.
    sleep(0.5) 
    
    proxy = HessianProxy(url)
        
    msg = proxy.nothing()
    assert None == msg
      
    msg = proxy.hello()
    assert SECRET_MESSAGE == msg
    
    try:
        proxy.askBitchy()
        assert False # should not get here
    except Exception as e:
        assert "Go away!" == e.testMessage 
    
    # What about UTF-8?
    padonkMessage = u"Пррревед обонентеги!"
    assert padonkMessage == proxy.echo(padonkMessage)
    
    callBlobTest(proxy)
    redirectTest(proxy)
    
    if True:
        from time import time 
        print "Some performance measurements..."
        count = 1000
        start = time()
        for _ in range(count):
            proxy.hello()
        fin = time()
        print "One call takes", 1000.0 * (fin - start) / count, "mSec."        

    srv.stop()

def realWorldTest1():
    import zlib, pickle     
    payload = zlib.compress(pickle.dumps("blah blah blah"))
    autoLoopBackTest(payload)


def callTestPublic(url):
    try:
        proxy = HessianProxy(url)
        
        proxy.nullCall()
        # In the next moment nothing continued to happen.
        
        assert "Hello, world" == proxy.hello()
        print '.',
        
        o = {1:"one", 2:"two"}
        assert o == proxy.echo(o)
        print '.',
        
        o = (-1, -2)
        assert list(o) == proxy.echo(o)
        print '.',
        
        o = ["S-word", "happen-s"]
        assert o == proxy.echo(o)
        print '.',
        
        a, b = 1902, 34
        assert (a - b) == proxy.subtract(a, b)
        print '.',
        
        # What about UTF-8?
        padonkRussianMessage = u"Превед!"
        assert padonkRussianMessage == proxy.echo(padonkRussianMessage)
        print '.',
                                                                                  
    except Exception as e:
        st = traceback.format_exc()
        if not warnConnectionRefused(e, url):
            print st
            raise e # re-thow


def sslTest():
    try:
        from OpenSSL import SSL # @UnusedImport
    except ImportError:
        print "Warning: Can not load OpenSSL module. SSL will not be tested."
        return
    
    import hessian.test.testSecure
    hessian.test.testSecure.testHttps()
     
def runList(funList):
    for fn in funList:
        fn()
        print '.',

if __name__ == "__main__":
    try:
        runList([
                 deserializeTest,
                 loopbackTestTypes,
                 serializeCallTest,
                 testHessianTypes,
                 testDatetime,
                 serializeReplyAndFaultTest,
                 referenceTest,
                 realWorldTest1,
                 lambda: callTestLocal("http://localhost:%d/" % TEST_PORT),
                 sslTest
                 ])
        
        print "Warning: Test with public service is disabled."
        # Following URL seems to be unavailable anymore
        # callTestPublic("http://www.caucho.com/hessian/test/basic/")
        
        print "\nTests passed."
        
    except Exception as e:
        st = traceback.format_exc()
        print "\nError occurred:\n", st
