import Pyro4


hungry1 = Pyro4.Proxy("PYRONAME:primaryBE")
hungry2 = Pyro4.Proxy("PYRONAME:secondaryBE1")
hungry3 = Pyro4.Proxy("PYRONAME:secondaryBE2")

def check():
    try:
        resp = hungry1.test()
        print("Primary back-end server selected\n")

        return hungry1

    except Exception:
        try:
            resp = hungry2.test()
            print("Secondary back-end server 1 selected\n")

            return hungry2
        except Exception:
            try:
                resp = hungry3.test()
                print("Secondary back-end server 2 selected\n")

                return hungry3
            except Exception:
                print("Error: cannot connect to back-end\n")
                exit(404)

@Pyro4.expose
class FrontEnd(object):

    def options(self):

        hungry = check()
        return hungry.options()

    def request(self, req):

        hungry = check()
        resp = None
        option = 1

        print("Request:", req)

        if "cancel" in req or "CANCEL" in req or "Cancel" in req:
            resp = [None, "Closing Just Hungry"]

        elif "types" in req or "list" in req or "1" in req:
            resp = ["types", hungry.foodTypes()]

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

            try:
                resp = hungry.order(item, postcode)
            except Exception:
                print("resp failed")

        print("Response:", resp)
        return resp


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FrontEnd)
ns.register("frontEnd", uri)

print("Front end server ready!")
daemon.requestLoop()
