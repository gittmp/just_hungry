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
            try:
                options = justHungry.options()
            except Exception:
                print(1)

            for o in options:
                print(o)

            # take input - number of option or name of option
            request = input("Option number: ").strip()

            if request == "cancel" or request == "CANCEL" or request == "Cancel":
                print("Closing Just Hungry\n")
                exit(1)

            else:
                try:
                    request = int(request)
                except ValueError:

                    print("Invalid option: select from above or cancel\n")
                    continue

            # response
            try:
                response = justHungry.request(request)
            except Exception:
                print(2)

            if response[0] == "types":
                print("\nFood types:")
                for food_type in response[1]:
                    print(food_type)

                select_type = input("Select type: ").strip()
                try:
                    rests = justHungry.request(["rests", select_type])
                except Exception:
                    print(3)

                print("\nRestaurants:")
                if rests[0]:
                    for rest in rests[1]:
                        print(rest)
                else:
                    print("Error:", rests[1], "\n")
                    continue

                select_rest = input("Select restaurant: ").strip()
                try:
                    menu = justHungry.request(["menu", select_rest])
                except Exception:
                    print(4)

                if menu[0]:
                    print("\nMenu:")
                    for item in menu[1]:
                        print(item)
                else:
                    print("Error:", menu[1])
                    continue

                order_item = input("Select item to order: ").strip()
                postcode = input("Please input your postcode: ").strip()

                try:
                    order = justHungry.request(["order", order_item, postcode])
                except Exception:
                    print(5)

                if order[0]:
                    print()
                    for line in order[1][1]:
                        print(line)
                    print("\nThank you for your order!\n")
                else:
                    print("Error:", order[1], "\n")
                    continue

            else:
                print("Error:", response[1], "\n")
                continue

        except Exception:
            print("Error: cannot connect to front end server")
            exit(1)

except KeyboardInterrupt:
    print("Closing Just Hungry\n")
