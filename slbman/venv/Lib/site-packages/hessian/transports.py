#
# Hessian protocol implementation
# This file contains pluggable transport mechanisms.
#
# Protocol specification can be found here:
# http://www.caucho.com/resin-3.0/protocols/hessian-1.0-spec.xtp
#
# Copyright 2006 Bernd Stolle (thebee at sourceforge net)
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
"""
Transports for Hessian.

Content:
* HessianTransport - abstract base class
* HTTPTransport - talk hessian over simple unencrypted HTTP,
    support for BasicAuthentication
"""

import base64
import httplib
from StringIO import StringIO
import urllib2
from common import HessianError

__revision__ = "$Rev: 89 $"
__version__ = "0.6.0"


AUTH_BASIC = "basic"


def getTransportForProtocol(protocol):
    """ Returns the appropriate transport for a protocol's URL scheme.
    Raises KeyError if no appropriate protocol found.
    """
    return {
        "http": BasicUrlLibTransport, 
        "https": BasicUrlLibTransport, 
    } [protocol]


class TransportError(Exception):
    """ Generic Exception for Transports
    """
    pass


class HessianTransport:
    """ Base class for all transports that can be used to talk 
    to a Hessian server. 
    """

    def __init__(self, uri, credentials):
        self._uri = uri
        self._credentials = credentials

    def request(self, outstream):
        " Send stream to server "
        raise HessianError("Hessian transport is incomplete:"
                           " Method is not implemented")
    
    
class BasicUrlLibTransport(HessianTransport):
    """ Transport handler that uses urllib2. 
    Basic authentication scheme is used. """
    
    def __init__(self, uri, credentials):
        HessianTransport.__init__(self, uri, credentials)
        # print "init:uri:", uri, "; cred:", self._credentials # debug
                
        if (self._credentials != None):            
            # TODO Make tests for authorization
            
            pman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            auth_handler = urllib2.HTTPBasicAuthHandler(pman)            
            auth_handler.add_password(None, # default realm
                                      uri, 
                                      self._credentials["username"], 
                                      self._credentials["password"])
            
            # TODO Add digest authorization handler here? 
            # HTTPDigestAuthHandler
            
            self._opener = urllib2.build_opener(auth_handler)
            
            # Following code allows sending authorization information in advance,
            # so single TCP request will suffice. Without it we'll rely on HTTP's 
            # authorization required response and authorization handlers.            
            # self._opener.addheaders["Authorization"] = "Basic %s" % base64.encodestring(
            #    "%s:%s" % (credentials["username"], 
            #               credentials["password"])).rstrip()
        else:
            self._opener = urllib2.build_opener()        
    
  
    def request(self, outstream):
        outstream.flush()
        req_data = outstream.read()        
        # print "request", map(lambda x : "%02x" % ord(x), req_data[:50]), "\n\t:", req_data[:50] # debug        
        r = urllib2.Request(self._uri, req_data)
        r.add_header("Content-Length", len(req_data))
        r.add_header("User-agent", "HessianPy/%s" % __version__)
        r.add_header("Content-type", "application/octet-stream")
        
        response = self._opener.open(r)
        result = StringIO(response.read())
        response.close()
        return result        
  
