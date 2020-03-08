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

    def options(self):

        hungry = check()
        return hungry.options()

    def request(self, req):

        hungry = check()
        resp = None

        if type(req) == int:
            if req == 1:
                resp = ["types", hungry.foodTypes()]
            else:
                resp = [False, "Cannot retrieve type"]

        elif req[0] == "rests":

            r_type = req[1]
            rests = hungry.restaurants(r_type)

            if rests[0]:
                resp = rests
            else:
                resp = [False, rests[1]]

        elif req[0] == "menu":

            rest = req[1]
            menu = hungry.menu(rest)

            if menu[0]:
                resp = menu
            else:
                resp = [False, menu[1]]

        elif req[0] == "order":

            item = req[1]
            postcode = req[2]

            resp = hungry.order(item, postcode)

        return resp


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FrontEnd)
ns.register("frontEnd", uri)

print("Front end server ready!")
daemon.requestLoop()
