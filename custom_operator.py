import csv
import datetime
from osbrain import Agent
import random

class Operator(Agent):
    pn = 1

    types = ['H', 'S', 'T']
    p_type = " "
    curr_price = 0
    log_file = ""
    auction_rec = []

    def on_init(self):
        # we create a communication of type publisher name "publish channel"
        self.bind('PUB', alias='publish_channel')
        current_date = datetime.datetime.now()
        self.log_file = 'log_' + str(current_date) + '.csv'
        self.auction_rec = []

    def send_new_product(self, message):
        # we send a new product to the merchants subscribed
        if(message == 'yes'):
            self.pn += 1
            self.p_type = self.types[random.randint(0, len(self.types) - 1)]

            self.curr_price = random.randint(20, 40)
        if(message == 'no'):
            self.curr_price -= 2
        self.send('publish_channel', {"product number": self.pn, "product type" : self.p_type, "price": self.curr_price})
   
    def reply(self, request):
        """
        Handle incoming requests on the REP socket.
        """
        if request == 'get_current_product':
            return {
                "product number": self.pn,
                "product type": self.p_type,
                "price": self.curr_price
            }
        return f"Unknown request: {request}"
    
    def write_csv(self):
        with open(self.log_file) as file:
            writer = csv.writer(file)
            writer.writerow(self.auction_rec)