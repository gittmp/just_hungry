# Just Hungry Distributed System

### Running System

0. Before running, the following modules need to be installed onto the desired computer:
- Install packages using the command:
- pip install *module*
- Modules:
...- Pyro4
...- json
...- urllib

1. Start name server from the command line.
- Use the following command from a terminal window:
- python -m Pyro4.naming

2. Start the back end servers from the command line.
- Use the following commands to start each of the three back end servers on seperate terminal windows:
- python BEServer1.py
- python BEServer2.py
- python BEServer3.py
- Any combination of these three servers can be ran.

3. Start the front end server from the command line:
- Use the following command on another terminal window:
- python FEServer.py

4. Finally, start the client program from the command line, through which you willinteract with the Just Hungry system.
- Use the following command from a terminal window
- python client.py

### Using the System

- Upon startup of the client program, in the terminal window you will be prompted with three options:
...1. List food types
...2. View order history
...3. Order item
- To select an option to continue with, either type in the corresponding number or write out the command (e.g. 'list food types', or 'simply types')

- If you select option 1, you will have to go through the following process to order an item:
...1. Input the type of food you would like, from the provided list.
...2. Input the restaurant you would like, from the provided list.
...3. Input your choice of food item, from the provided list.
...4. Enter your postcode, for delivery.
- If this is successful, you will be alerted and your address displayed.
- If an error occurs (e.g. the food item is out of stock) you will be alerted.

- If you select option 2, the terminal will display all previous orders you have made in this session.

- If you select option 3, you will be prompted to input the desired restaurant and food item you wish fo order, along with your postcode.
- If this is successful, you will be alerted and your address displayed.
- If an error occurs (e.g. the specified restaurant/item does not exist) you will be alerted.

- You can enter the command 'cancel' to cancel the ordering session.

### Errors

- If an error occurs on one of the back end or front end servers, the error message will be displayed in the corresponding terminal.


### External Resources

- The Just Hungry system implements the following web services (in presedence order) to display the user's address on inout of a postcode:
- postcodes.io
- getthedata.com



