# python -m Pyro4.naming
import Pyro4
import json
import urllib
import urllib.request


@Pyro4.expose
# services program in class (name server)
class BackEnd(object):
    def test(self):
        return 1

    def order(self, item):
        return "Ordering your {}!".format(item)

    def foodTypes(self):
        types = ["British", "Italian", "Indian", "Chinese", "Burgers"]
        return types

    def getAddress(self, postcode):
        postcode = postcode.replace(" ", "+")
        url = 'http://api.getthedata.com/postcode/' + postcode
        req = urllib.request.urlopen(url)
        resp_str = req.read().decode('utf-8')
        resp_js = json.loads(resp_str)
        return resp_js


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("secondaryBE1", uri)

print("Secondary back-end server 1 ready!")
daemon.requestLoop()
