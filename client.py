import Pyro4
import time


# loop while user still wants to make orders - close on 'cancel' or ^C
try:
    while 1:
        try:
            # link to RMI server through name server
            justHungry = Pyro4.Proxy("PYRONAME:frontEnd")

            # display available options (actions)
            options = justHungry.options()

            for o in options:
                print(o)

            # take input - number of option or name of option
            request = input("Option: ").strip()

            # response
            try:
                response = justHungry.request(request)
            except Exception:
                print("Error: Just Hungry server is down")
                continue

            if response[0] == "types":
                print("\nFood types:")
                for food_type in response[1]:
                    print(food_type)

                select_type = input("Select type: ").strip()
                try:
                    rests = justHungry.request(["rests", select_type])
                except Exception:
                    print("cannot get type")
                    continue

                if rests[0]:
                    print("\nRestaurants:")
                    for rest in rests[1]:
                        print(rest)
                else:
                    print(rests[1], "\n")
                    continue

                select_rest = input("Select restaurant: ").strip()
                menu = justHungry.request(["menu", select_rest])

                if menu[0]:
                    print("\nMenu:")
                    for item in menu[1]:
                        print(item)
                else:
                    print(menu[1], "\n")
                    continue

                order_item = input("Select item to order: ").strip()
                postcode = input("Please input your postcode: ").strip()

                order = justHungry.request(["place_ord", order_item, postcode])

                if order[0]:
                    print()
                    for line in order[1]:
                        print(line)
                    print("\nThank you for your order!\n")
                else:
                    print(order[1], "\n")
                    continue

            elif response[0] == "history":

                print("\nOrder history:")
                orders = list(response[1].values())
                no_orders = len(orders[0])
                if no_orders > 0:
                    for i in range(no_orders):
                        print("Type = " + orders[0][i] + ", Restaurant = " + orders[1][i])
                        print("Item = " + orders[2][i] + ", Delivery address = " + orders[3][i])
                        print()
                else:
                    print("No previous orders\n")

            elif response[0] == "checkout":
                rest = input("Input restaurant you wish to order from: ")
                food = input("Input food order you wish to make: ")
                postcode = input("Input your delivery postcode: ")
                order = justHungry.request(["place_ord", food, postcode, rest])

                if order[0]:
                    print()
                    for line in order[1]:
                        print(line)
                    print("\nThank you for your order!\n")
                else:
                    print(order[1], "\n")
                    continue

            elif response[0] is None:
                print(response[1])
                exit(1)

            else:
                print(response[1], "\n")
                continue

        except Pyro4.core.errors.CommunicationError:
            print("Error: cannot connect to server")
            time.sleep(1)
            continue

except KeyboardInterrupt:
    print("Closing Just Hungry\n")
