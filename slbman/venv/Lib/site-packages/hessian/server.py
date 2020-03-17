#
# Hessian protocol implementation
# This file contains simple RPC server code.
#
# Protocol specification can be found here:
# http://www.caucho.com/resin-3.0/protocols/hessian-1.0-spec.xtp
#
# Copyright 2006-2007 Petr Gladkikh (batyi at users sourceforge net)
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
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import hessian
from StringIO import StringIO
import traceback
import socket


__revision__ = "$Rev: 89 $"


class HessianHTTPRequestHandler(BaseHTTPRequestHandler):    
    """Subclasses should create clss's member message_map which maps method 
    names into function objects """
    
    MAX_CHUNK_SIZE = 2 ^ 12
    
    def do_POST(self):        
        try:
            ctx = hessian.ParseContext(self.rfile)
            (method, headers, params) = hessian.Call().read(ctx, ctx.read(1))
        except Exception as e:
            self.send_error(500, "Can not parse call request. Error: " + str(e))
            return
      
        if not self.message_map.has_key(method):    
            self.send_error(500, "Method '" + method + "' is not found")
            return
        
        succeeded = True
        try:
            result = self.message_map[method](*([self] + params))
        except Exception as e:
            stackTrace = traceback.format_exc()
            succeeded = False                        
            result = {"stackTrace" : stackTrace, "args" : e.args}
            result.update(e.__dict__)             
        
        try:
            sio = StringIO()
            hessian.Reply().write(
                          hessian.WriteContext(sio),
                          (headers, succeeded, result))
            reply = sio.getvalue()
        except Exception:
            stackTrace = traceback.format_exc()
            # todo write this to logs
            self.send_error(500, "Can not send response for '" + method + "'\n" + stackTrace)
            return            
        
        self.send_response(200, "OK")
        self.send_header("Content-type", "application/octet-stream")                
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

class ServerStoppedError(Exception):
    pass

class StoppableHTTPServer(HTTPServer):
    """
    Code adapted from Python CookBook
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/425210
    """
    
    def server_bind(self):
        HTTPServer.server_bind(self)
        self.run = True

    def get_request(self):
        while self.run:
            return self.socket.accept()
        raise ServerStoppedError()

    def stop(self):
        self.run = False

    def serve(self):
        try:
            while self.run:
                self.handle_request()
        except ServerStoppedError:
            return
        

# ---------------------------------------------------------
# Server usage example


def hello():
    return "Hello, from HessianPy!"


class TestHandler(HessianHTTPRequestHandler):      
    message_map = {"hello" : hello}        
    
                
if __name__ == "__main__":
    
    # Example code     
    print "Starting test server"
    server_address = ('localhost', 9001)
    httpd = StoppableHTTPServer(server_address, TestHandler)
    print "Serving from ", server_address
    httpd.serve()
    import time
    time.sleep(200)
    httpd.stop()
    print "Stopping test server"
    
