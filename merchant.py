from osbrain import Agent


class Merchant(Agent):
    budget = 100
    preference = None

    current_type = None
    current_price = None

    def on_init(self):
        pass

    def on_new_msg(self, msg):
        self.log_info(msg)
        self.current_type = msg['product type']
        self.current_price = msg['price']

    def setPreference(self, pref):
        self.preference = pref

    def send_recv(self, address, message):
        return self.choice()

    def choice(self):
        if(self.current_type == self.preference):
            if (self.current_type <= 3 * self.budget // 4):
                return {"yes"}
            else:
                return {"no"}
        else:
            if(self.current_type <= self.budget // 2):
                return {"yes"}
            else:
                return {"no"}
        # return {"yes"}
