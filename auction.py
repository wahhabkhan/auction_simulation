from custom_operator import Operator
from merchant import Merchant
import osbrain
import random
import time
import datetime
import csv

def message_handler(agent, message):
    print(f"[{agent.name}] Received message: {message}")

def auction(num_m, num_f, a_type):
    # Get current date for unique filenames
    current_date = datetime.datetime.now()
    setup_file = 'setup_' + current_date.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
    log_file = 'log_' + current_date.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
    
    # Initialize the lists to hold auction and setup records
    setup_rec = []
    auction_rec = []

    # Start the Operator agent
    op = Operator()
    addr = op.bind('REP', alias='publish_channel', handler='reply')

    # Allow time for binding to complete
    print("Waiting for operator agent to bind...")
    time.sleep(2)  # Increase if necessary to give the operator time to bind

    # Possible preferences for Merchants
    fTypes = ['H', 'S', 'T']
    f = 0
    mList = []

    # Create Merchant agents and set their preferences
    for i in range(num_m):
        m = Merchant()
        pref = ""

        if a_type == 'R':  # Random preference
            pref = fTypes[random.randint(0, 2)]
        elif a_type == 'NR':  # Non-Random (Cyclic) preference
            pref = fTypes[f]
            f = (f + 1) % 3  # Cycle through H, S, T

        m.setPreference(pref)
        setup_rec.append([str(i + 1), str(pref), str(100)])  # Example setup record: [Merchant ID, Preference, Price]
        m.connect(op.addr('publish_channel'), alias='publish_channel', handler=message_handler)
        mList.append(m)

    # Write the setup records to a CSV file
    with open(setup_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Merchant ID', 'Preference', 'Price'])  # Header
        writer.writerows(setup_rec)

    # Run the auction for the number of products
    for i in range(num_f):
        isBid = 'no'
        op.send_new_product('yes')  # Announce a new product

        # Wait for a bid from merchants
        while isBid == 'no':
            time.sleep(0.1)  # Wait before checking again
            for j in mList:
                if j.recv('publish_channel') == 'yes':
                    isBid = 'yes'
            op.send_new_product('no')  # Reduce product price

    op.write_csv()
