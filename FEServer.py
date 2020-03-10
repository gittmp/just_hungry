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
        resp = [False, "Error: invalid request"]

        print("Request:", req)

        if "cancel" in req or "Cancel" in req:
            resp = [None, "Closing Just Hungry"]

        elif "types" in req or "list" in req or "1" in req:
            resp = ["types", hungry.food_types()]

        elif "history" in req or "2" in req:
            resp = ["history", hungry.get_history()]

        elif "order" in req or "3" in req:
            resp = ["checkout"]

        elif req[0] == "rests":

            r_type = req[1]
            resp = hungry.restaurants(r_type)

        elif req[0] == "menu":

            rest = req[1]
            resp = hungry.menu(rest)

        elif req[0] == "place_ord":

            item = req[1]
            postcode = req[2]

            if len(req) == 3:
                try:
                    resp = hungry.order(item, postcode, None)
                except Exception:
                    print("resp failed")
            else:
                rest = req[3]
                resp = hungry.order(item, postcode, rest)
                print("resp failed")

        print("Response:", resp)
        return resp


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FrontEnd)
ns.register("frontEnd", uri)

print("Front end server ready!")
daemon.requestLoop()
