# python -m Pyro4.naming
import Pyro4


@Pyro4.expose
# services program in class (name server)
class BackEnd(object):
    def order(self, item):
        return "Ordering your {}!".format(item)
    def foodTypes(self):
        types = ["British", "Italian", "Indian", "Chinese", "Burgers"]
        return types


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("primaryBE", uri)

print("Primary back-end server ready!")
daemon.requestLoop()
