import Pyro4


hungry1 = Pyro4.Proxy("PYRONAME:primaryBE")
hungry2 = Pyro4.Proxy("PYRONAME:secondaryBE1")
hungry3 = Pyro4.Proxy("PYRONAME:secondaryBE2")

def check():
    try:
        resp = hungry1.test()
        return hungry1
    except Exception:
        try:
            resp = hungry2.test()
            return hungry2
        except Exception:
            try:
                resp = hungry3.test()
                return hungry3
            except Exception:
                exit(404)

@Pyro4.expose
class FrontEnd(object):
    def request(self, req):
        hungry = check()
        print("Thanks for your request: " + req)
        resp = None
        if req == "list food types":
            resp = hungry.foodTypes()
        return resp


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FrontEnd)
ns.register("frontEnd", uri)

print("Front end server ready!")
daemon.requestLoop()
