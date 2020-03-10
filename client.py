import Pyro4
import Pyro4.errors
import time


# loop while user still wants to make orders - close on 'cancel' or ^C
try:
    while 1:
        try:
            # link to RMI server through name server
            justHungry = Pyro4.Proxy("PYRONAME:frontEnd")

            # display available options (actions) for user
            options = justHungry.options()

            for o in options:
                print(o)

            # take input - number of option or name of option
            request = input("Option: ").strip()

            # response
            response = justHungry.request(request)

            if response[0] == "types":
                # if types is selected, display types of food available
                print("\nFood types:")
                for food_type in response[1]:
                    print(food_type)

                # choose a type of food
                select_type = input("Select type: ").strip()
                rests = justHungry.request(["rests", select_type])

                # if exists, display available restaurants of that type
                if rests[0]:
                    print("\nRestaurants:")
                    for rest in rests[1]:
                        print(rest)
                else:
                    print(rests[1], "\n")
                    continue

                # choose a restaurant to order from
                select_rest = input("Select restaurant: ").strip()
                menu = justHungry.request(["menu", select_rest])

                # if available, display the menu for that restaurant
                if menu[0]:
                    print("\nMenu:")
                    for item in menu[1]:
                        print(item)
                else:
                    print(menu[1], "\n")
                    continue

                # select an item from the menu to order, and provide your delivery postcode
                order_item = input("Select item to order: ").strip()
                postcode = input("Please input your postcode: ").strip()
                order = justHungry.request(["place_ord", order_item, postcode])

                # if item available, and your postcode is correct, place the order and give confirmation to the customer
                if order[0]:
                    print()
                    for line in order[1]:
                        print(line)
                    print("\nThank you for your order!\n")
                else:
                    print(order[1], "\n")
                    continue

            # if customer wishes to view their order history
            elif response[0] == "history":

                # retrieve customers order history
                orders = list(response[1].values())
                no_orders = len(orders[0])

                # if history exists, display it
                print("\nOrder history:")
                if no_orders > 0:
                    for i in range(no_orders):
                        print("Type = " + orders[0][i] + ", Restaurant = " + orders[1][i])
                        print("Item = " + orders[2][i] + ", Delivery address = " + orders[3][i])
                        print()
                else:
                    print("No previous orders\n")

            # if customer wishes to
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
            print("Error: cannot connect to Just Hungry")
            time.sleep(1)
            continue

except KeyboardInterrupt:
    print("Closing Just Hungry\n")
