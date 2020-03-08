import Pyro4


# link to RMI server through name server
try:
    justHungry = Pyro4.Proxy("PYRONAME:frontEnd")
except Exception:
    print("Error: cannot connect to name server")
    exit(1)

# loop while user still wants to make orders - close on 'cancel' or ^C
try:
    while 1:
        # display available options (actions)
        try:
            options = justHungry.options()
        except Exception:
            print("Error: cannot connect to front end server")
            exit(1)

        for o in options:
            print(o)

        # take input - number of option or name of option
        request = input("Option number: ").strip()

        if request == "cancel" or request == "CANCEL" or request == "Cancel":
            print("Closing Just Hungry")
            exit(1)

        else:
            try:
                request = int(request)
            except ValueError:
                print("Invalid option: select from above or cancel")
                continue

        # response
        response = justHungry.request(request)
        print("Response:")

        if response[0] == "types":
            print("Food types:")
            for food_type in response[1]:
                print(food_type)

            select_type = input("Select type: ").strip()
            rests = justHungry.request(["rests", select_type])

            print("Restaurants:")
            if rests[0]:
                for rest in rests:
                    print(rest)
            else:
                print("Error")

            select_rest = input("Select restaurant: ").strip()
            menu = justHungry.request(["menu", select_rest])

            print("Menu:")
            for item in menu:
                print(item)

            order_item = input("Select item to order: ").strip()
            postcode = input("Please input your postcode: ").strip()

            order = justHungry.request(["order", order_item, postcode])
            if order[0]:
                for line in order[1][1]:
                    print(line)
            else:
                print("Error:", order[1])

        else:
            print("Error:", response[1])

except KeyboardInterrupt:
    print("Closing Just Hungry")
