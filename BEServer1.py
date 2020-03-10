# python -m Pyro4.naming
import Pyro4
import Pyro4.errors
import json
import urllib
import urllib.request
import urllib.error


secondaryServer1 = Pyro4.Proxy("PYRONAME:secondaryBE1")
secondaryServer2 = Pyro4.Proxy("PYRONAME:secondaryBE2")


@Pyro4.expose
# services program in class (name server)
class BackEnd(object):
    try:
        history = secondaryServer1.get_history()
    except Pyro4.errors.CommunicationError:
        try:
            history = secondaryServer2.get_history()
        except Pyro4.errors.CommunicationError:
            history = {"types": [], "restaurants": [], "items": [], "postcodes": []}

    actions = [
        "1) list food types",
        "2) View order history",
        "3) Order item"
    ]

    rest_types = {
        "British": ["Wetherspoons", "Greggs", "Bells"],
        "Italian": ["La Spaghettata", "Uno Momento", "Zizzi"],
        "Mexican": ["Zaps", "Barrio"]
    }

    food = {
        "Wetherspoons": {"Margarita pizza - £6.00": True, "Cheeseburger - £4.50": True, "Chicken wrap - £3.00": False},
        "Greggs": {"Sausage roll - £1.00": True, "Steak bake - £1.50": True, "Vegan sausage roll - £1.00": True},
        "Bells": {"Fish and chips - £6.50": True, "Small chips - £2.00": False, "Sausage and chips - £6.00": True},
        "La Spaghettata": {"La Reine pizza - £8.20": True, "Lasagna - £7.00": True, "Spaghetti bolognese - £6.00": True},
        "Uno Momento": {"Sharing platter - £10.80": True, "Lasagna - £8.50": False, "Shellfish linguine - £9.00": True},
        "Zizzi": {"Pollo pesto - £8.50": False, "Pizza rustica - £12.00": True, "Carbonara - £9.99": True},
        "Zaps": {"Burrito - £5.00": True, "Quesadillas - £4.50": True, "Enchiladas - £4.50": True},
        "Barrio": {"Beef taco - £3.80": True, "Vegetarian taco - £3.80": False}
    }

    def test(self):

        return 1

    def get_history(self):

        self.reset_all_histories()

        return self.history

    def update_history(self, event):

        key = event[0]
        value = event[1]

        self.history[key].append(value)

        return 1

    def reset_history(self):

        hist_arrays = list(self.history.values())
        lens = []

        for arr in hist_arrays:
            lens.append(len(arr))
        stable_len = min(lens)

        for key in list(self.history.keys()):
            self.history[key] = self.history[key][:stable_len]

        return 1

    def reset_all_histories(self):

        self.reset_history()

        try:
            secondaryServer1.reset_history()
        except Pyro4.errors.CommunicationError:
            print("Error: cannot connect to secondary back-end server 1")
        try:
            secondaryServer2.reset_history()
        except Pyro4.errors.CommunicationError:
            print("Error: cannot connect to secondary back-end server 2")

        return 1

    def update_all_histories(self, event):

        try:
            secondaryServer1.update_history(event)
        except Pyro4.errors.CommunicationError:
            print("Error: cannot connect to secondary back-end server 1")
        try:
            secondaryServer2.update_history(event)
        except Pyro4.errors.CommunicationError:
            print("Error: cannot connect to secondary back-end server 2")

        return 1

    def options(self):

        poss_options = self.actions

        return poss_options

    def food_types(self):

        types = self.rest_types.keys()

        return types

    def restaurants(self, r_type):

        restaurants = self.rest_types
        event = ["types"]

        try:
            rests = restaurants[r_type]
            self.history["types"].append(r_type)
            event.append(r_type)
            self.update_all_histories(event)

            return [True, rests]

        except KeyError:
            try:
                rest_keys = restaurants.keys()

                for key in rest_keys:
                    if r_type == key.lower():
                        r_type = key

                rests = restaurants[r_type]
                self.history["types"].append(r_type)
                event.append(r_type)
                self.update_all_histories(event)

                return [True, rests]

            except KeyError:
                error = "Type not found"

                return [False, error]

    def menu(self, rest):

        menus = self.food
        event = ["restaurants"]

        try:
            menu = menus[rest].keys()
            self.history["restaurants"].append(rest)
            event.append(rest)
            self.update_all_histories(event)

            return [True, menu]

        except KeyError:
            try:
                menu_keys = menus.keys()
                for key in menu_keys:
                    if rest == key.lower():
                        rest = key
                menu = menus[rest].keys()

                self.history["restaurants"].append(rest)
                event.append(rest)
                self.update_all_histories(event)

                return [True, menu]

            except KeyError:
                error = "Restaurant not found"
                self.reset_all_histories()

                return [False, error]

    def stock(self, item, rest):

        rest_found = False

        if rest is None:
            rest_history = self.history["restaurants"]
            restaurant = rest_history[len(rest_history) - 1]
            rest_found = True
        else:
            rests = list(self.rest_types.values())
            for i in range(len(rests)):
                for j in range(len(rests[i])):
                    if rest == rests[i][j] or rest == rests[i][j].lower():
                        index = i
                        restaurant = rests[i][j]
                        rest_found = True
            if rest_found:
                r_type = list(self.rest_types.keys())[index]
                self.history["types"].append(r_type)
                self.history["restaurants"].append(restaurant)
            else:
                error = "Error: cannot find restaurant"
                in_stock = [False, error]

        if rest_found:
            current_stock = self.food[restaurant]
            full_item = ""
            event = ["items"]

            for meal in current_stock.keys():
                if item in meal or item in meal.lower():
                    full_item = meal
                    break

            if len(full_item) > 0:
                availability = current_stock[full_item]
                if availability:
                    in_stock = [True]
                else:
                    error = "Error: item out of stock"
                    in_stock = [False, error]

                self.history["items"].append(full_item)
                event.append(full_item)

                self.update_all_histories(event)

            else:
                error = "Error: no such item"
                in_stock = [False, error]

        return in_stock

    def address(self, postcode):

        postcode = postcode.replace(" ", "")
        url = 'https://api.postcodes.io/postcodes/' + postcode

        try:
            req = urllib.request.urlopen(url)
            source = 1

        except (urllib.error.HTTPError, urllib.error.URLError):
            try:
                url = 'http://api.getthedata.com/postcode/' + postcode
                req = urllib.request.urlopen(url)
                source = 2

            except (urllib.error.HTTPError, urllib.error.URLError):
                error = "Error: cannot validate postcode"
                self.reset_all_histories()

                return [False, error]

        resp_str = req.read().decode('utf-8')
        resp_js = json.loads(resp_str)
        event = ["postcodes"]

        if source == 1 and resp_js["status"] == 200:

            full_postcode = resp_js["result"]["postcode"]

            address_info = [
                "Delivering your order to:",
                "Postcode: " + full_postcode,
                "Longitude: " + str(resp_js["result"]["longitude"]),
                "Latitude: " + str(resp_js["result"]["latitude"]),
                resp_js["result"]["admin_ward"],
                resp_js["result"]["parliamentary_constituency"],
                resp_js["result"]["admin_district"]
            ]

            self.history["postcodes"].append(full_postcode)
            event.append(full_postcode)
            self.update_all_histories(event)

            return [True, address_info]

        elif source == 2 and resp_js["status"] == "match":

            full_postcode = resp_js["data"]["postcode"]

            address_info = [
                "Delivering your order to:",
                "Postcode: " + full_postcode,
                "Longitude: " + str(resp_js["data"]["longitude"]),
                "Latitude: " + str(resp_js["data"]["latitude"])
            ]

            self.history["postcodes"].append(full_postcode)
            event.append(full_postcode)
            self.update_all_histories(event)

            return [True, address_info]

        else:
            self.reset_all_histories()

            return [False, resp_js["error"]]

    def order(self, item, postcode, rest):

        in_stock = self.stock(item, rest)

        if in_stock[0]:
            resp = self.address(postcode)
        else:
            self.reset_all_histories()

            resp = in_stock

        return resp


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("primaryBE", uri)

print("Primary back-end server ready!")
daemon.requestLoop()
