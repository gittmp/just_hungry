# python -m Pyro4.naming
import Pyro4
import json
import urllib
import urllib.request

@Pyro4.expose
# services program in class (name server)
class BackEnd(object):

    history = {}

    actions = [
        "1) list food types",
        "2) order item"
    ]

    rest_types = {
            "British": ["Spoons", "Greggs", "Bells"],
            "Italian": ["Spags", "Uno Momento", "Zizzi"],
            "Mexican": ["Zaps", "Barrio"]
    }

    food = {
            "Spoons": {"Margarita Pizza - £6.00": True, "Cheeseburger - £4.50": True, "Chicken wrap - £3.00": False},
            "Greggs": {"Sausage roll - £1.00": True, "Steak bake - £1.50": True, "Vegan sausage roll - £1.00": True},
            "Bells": {"Fish and chips - £6.50": True, "Chips - £2.00": False, "Sausage and chips - £6.00": True},
            "Spags": {"La Reine pizza - £8.20": True, "Lasagne - £7.00": True, "Spagetti bolonese - £6.00": True},
            "Uno Momento": {"Sharing platter - £10.80": True, "Lasagne - £8.50": False, "Shellfish linguine - £9.00": True},
            "Zizzi": {"Pollo pesto - £8.50": False, "Pizza rustica - £12.00": True, "Carbonara - £9.99": True},
            "Zaps": {"Burrito - £5.00": True, "Quesadillas - £4.50": True, "Enchiladas - £4.50": True},
            "Barrio": {"Beef taco - £3.80": True, "Vegetarian taco - £3.80": False}
        }

    def test(self):
        return 1

    def options(self):

        poss_options = self.actions

        return poss_options

    def foodTypes(self):

        types = self.rest_types.keys()

        return types

    def restaurants(self, r_type):

        self.history.update({"type": r_type})
        restaurants = self.rest_types

        try:
            rests = restaurants[r_type]
            return [True, rests]
        except KeyError:
            error = "Type not found"
            return [False, error]

    def menu(self, rest):

        self.history.update({"restaurant": rest})
        menus = self.food

        try:
            menu = menus[rest]
            return [True, menu]
        except KeyError:
            error = "Restaurant not found"
            return [False, error]

    def stock(self, item):

        restaurant = self.history["restaurant"]
        current_stock = self.food[restaurant]
        in_stock = False
        full_item = ""

        for meal in current_stock.keys():
            if item in meal:
                full_item = meal
                break

        if len(full_item) > 0:
            in_stock = current_stock[full_item]

        return in_stock

    def address(self, postcode):

        postcode = postcode.replace(" ", "")
        url = 'https://api.postcodes.io/postcodes/' + postcode
        req = urllib.request.urlopen(url)
        resp_str = req.read().decode('utf-8')
        resp_js = json.loads(resp_str)

        if resp_js["status"] == 200:

            address_info = [
                "Delivering your order to:",
                "Postcode: " + resp_js["result"]["postcode"],
                "Longitude: " + str(resp_js["result"]["longitude"]),
                "Latitude: " + str(resp_js["result"]["latitude"]),
                resp_js["result"]["admin_ward"],
                resp_js["result"]["parliamentary_constituency"],
                resp_js["result"]["admin_district"]
            ]

            return [True, address_info]

        else:

            return [False, resp_js["error"]]


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("primaryBE", uri)

print("Primary back-end server ready!")
daemon.requestLoop()
