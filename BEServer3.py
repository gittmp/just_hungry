# python -m Pyro4.naming
import Pyro4
import json
import urllib
import urllib.request

primaryServer = Pyro4.Proxy("PYRONAME:primaryBE")
secondaryServer1 = Pyro4.Proxy("PYRONAME:secondaryBE1")


@Pyro4.expose
# services program in class (name server)
class BackEnd(object):

    try:
        history = primaryServer.get_history()
    except Exception:
        try:
            history = secondaryServer1.get_history()
        except Exception:
            history = {"types": [], "restaurants": [], "items": [], "postcodes": []}

    actions = [
        "1) list food types",
        "2) View order history",
        "3) Order item"
    ]

    rest_types = {
        "British": ["Spoons", "Greggs", "Bells"],
        "Italian": ["Spags", "Uno Momento", "Zizzi"],
        "Mexican": ["Zaps", "Barrio"]
    }

    food = {
        "Spoons": {"Margarita pizza - £6.00": True, "Cheeseburger - £4.50": True, "Chicken wrap - £3.00": False},
        "Greggs": {"Sausage roll - £1.00": True, "Steak bake - £1.50": True, "Vegan sausage roll - £1.00": True},
        "Bells": {"Fish and chips - £6.50": True, "Small chips - £2.00": False, "Sausage and chips - £6.00": True},
        "Spags": {"La Reine pizza - £8.20": True, "Lasagne - £7.00": True, "Spagetti bolonese - £6.00": True},
        "Uno Momento": {"Sharing platter - £10.80": True, "Lasagne - £8.50": False, "Shellfish linguine - £9.00": True},
        "Zizzi": {"Pollo pesto - £8.50": False, "Pizza rustica - £12.00": True, "Carbonara - £9.99": True},
        "Zaps": {"Burrito - £5.00": True, "Quesadillas - £4.50": True, "Enchiladas - £4.50": True},
        "Barrio": {"Beef taco - £3.80": True, "Vegetarian taco - £3.80": False}
    }

    def test(self):

        try:
            print("Primary history:", primaryServer.history)
        except Exception:
            print("Primary server down")

        try:
            print("Secondary 1 history:", secondaryServer1.get_history())
        except Exception:
            print("Secondary server 1 down")

        print("Secondary 2 history:", self.history, "\n")

        return 1

    def get_history(self):

        return self.history

    def update_history(self, event):

        key = event[0]
        value = event[1]

        self.history[key].append(value)
        print("Updating history:", self.history, "\n")

        return 1

    def reset_history(self):

        hist_arrays = list(self.history.values())
        lens = []

        for arr in hist_arrays:
            lens.append(len(arr))
        stable_len = min(lens)

        for key in list(self.history.keys()):
            self.history[key] = self.history[key][:stable_len]

        print("Resetting history:", self.history, "\n")

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

            try:
                primaryServer.update_history(event)
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.update_history(event)
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

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

                try:
                    primaryServer.update_history(event)
                except Exception:
                    print("Error: cannot connect to primary back-end server")
                try:
                    secondaryServer1.update_history(event)
                except Exception:
                    print("Error: cannot connect to secondary back-end server 1")

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

            try:
                primaryServer.update_history(event)
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.update_history(event)
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

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

                try:
                    primaryServer.update_history(event)
                except Exception:
                    print("Error: cannot connect to primary back-end server")
                try:
                    secondaryServer1.update_history(event)
                except Exception:
                    print("Error: cannot connect to secondary back-end server 1")

                return [True, menu]
            except KeyError:
                error = "Restaurant not found"
                self.reset_history()

                try:
                    primaryServer.reset_history()
                except Exception:
                    print("Error: cannot connect to primary back-end server")
                try:
                    secondaryServer1.reset_history()
                except Exception:
                    print("Error: cannot connect to secondary back-end server 1")

                return [False, error]

    def stock(self, item, rest):

        if rest is None:
            rest_history = self.history["restaurants"]
            restaurant = rest_history[len(rest_history) - 1]
        else:
            restaurant = rest

        current_stock = self.food[restaurant]
        in_stock = False
        full_item = ""
        event = ["items"]

        for meal in current_stock.keys():
            if item in meal or item in meal.lower():
                full_item = meal
                break

        if len(full_item) > 0:
            in_stock = current_stock[full_item]
            self.history["items"].append(full_item)
            event.append(full_item)

            try:
                primaryServer.update_history(event)
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.update_history(event)
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

        else:
            print("Error: no such item")

        return in_stock

    def address(self, postcode):

        print("getting url")
        postcode = postcode.replace(" ", "")
        try:
            url = 'https://api.postcodes.io/postcodes/' + postcode
        except Exception:
            print("Falied to retrieve url")
        print("got url")
        req = urllib.request.urlopen(url)
        resp_str = req.read().decode('utf-8')
        resp_js = json.loads(resp_str)
        event = ["postcodes"]

        if resp_js["status"] == 200:
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

            try:
                primaryServer.update_history(event)
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.update_history(event)
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

            return [True, address_info]

        else:
            self.reset_history()

            try:
                primaryServer.reset_history()
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.reset_history()
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

            return [False, resp_js["error"]]

    def order(self, item, postcode, rest):
        in_stock = self.stock(item, rest)

        if in_stock:
            address_info = self.address(postcode)
            if address_info[0]:
                resp = [True, address_info]
            else:
                error = "Invalid postcode"

                resp = [False, error]
        else:
            error = "Item out of stock"
            self.reset_history()

            try:
                primaryServer.reset_history()
            except Exception:
                print("Error: cannot connect to primary back-end server")
            try:
                secondaryServer1.reset_history()
            except Exception:
                print("Error: cannot connect to secondary back-end server 1")

            resp = [False, error]

        return resp


# locate name server and link it to this RMI server
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(BackEnd)
ns.register("secondaryBE2", uri)

print("Secondary back-end server 2 ready!")
daemon.requestLoop()
