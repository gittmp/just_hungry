import Pyro4

# get input from user

request = input("Request: ").strip()

# link to RMI server through name server
justHungry = Pyro4.Proxy("PYRONAME:frontEnd")

# response
response = justHungry.request(request)
print("Response:")
if type(response) == list:
    for item in response:
        print(item)
else:
    print(response)
