# python -m Pyro4.naming
import Pyro4
import json
import urllib
import urllib.request

@Pyro4.expose
# services program in class (name server)
class BackEnd(object):

    history = {"types": [], "restaurants": [], "items": [], "postcodes": []}

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
            "Spoons": {"Margarita pizza - £6.00": True, "Cheeseburger - £4.50": True, "Chicken wrap - £3.00": False},
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

        restaurants = self.rest_types

        try:
            print(r_type)
            rests = restaurants[r_type]
            self.history["types"].append(r_type)
            return [True, rests]
        except KeyError:
            try:
                rest_keys = restaurants.keys()
                for key in rest_keys:
                    if r_type == key.lower():
                        r_type = key
                rests = restaurants[r_type]
                self.history["types"].append(r_type)
                return [True, rests]
            except KeyError:
                error = "Type not found"
                return [False, error]

    def menu(self, rest):

        menus = self.food

        try:
            menu = menus[rest].keys()
            self.history["restaurants"].append(rest)
            return [True, menu]
        except KeyError:
            try:
                menu_keys = menus.keys()
                for key in menu_keys:
                    if rest == key.lower():
                        rest = key
                menu = menus[rest].keys()
                self.history["restaurants"].append(rest)
                return [True, menu]
            except KeyError:
                error = "Restaurant not found"
                return [False, error]

    def stock(self, item):

        rest_history = self.history["restaurants"]
        restaurant = rest_history[len(rest_history)-1]
        current_stock = self.food[restaurant]
        in_stock = False
        full_item = ""

        for meal in current_stock.keys():
            if item in meal or item in meal.lower():
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

    def order(self, item, postcode):

        in_stock = self.stock(item)

        if in_stock:
            address_info = self.address(postcode)
            if address_info[0]:
                resp = [True, address_info]
            else:
                error = "Invalid postcode"
                resp = [False, error]
        else:
            error = "Item out of stock"
            resp = [False, error]

        return resp


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("primaryBE", uri)

print("Primary back-end server ready!")
daemon.requestLoop()
