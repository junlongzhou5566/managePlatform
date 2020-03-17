#
# Simplest hessian client example
#

import client

proxy = client.HessianProxy("http://www.caucho.com/hessian/test/basic")
print proxy.hello()


