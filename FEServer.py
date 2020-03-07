import Pyro4


hungry1 = Pyro4.Proxy("PYRONAME:primaryBE")
hungry2 = Pyro4.Proxy("PYRONAME:secondaryBE1")
hungry3 = Pyro4.Proxy("PYRONAME:secondaryBE2")


@Pyro4.expose
class FrontEnd(object):
    def request(self, req):
        print("Thanks for your request: " + req)
        resp = None
        if req == "list food types":
            try:
                resp = hungry1.foodTypes()
                print("Response given from primary server")
            except Exception:
                try:
                    resp = hungry2.foodTypes()
                    print("Response given from secondary server 1")
                except Exception:
                    try:
                        resp = hungry3.foodTypes()
                        print("Response given from secondary server 2")
                    except Exception:
                        print("All servers down")
                        exit(404)
        return resp


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FrontEnd)
ns.register("frontEnd", uri)

print("Front end server ready!")
daemon.requestLoop()
