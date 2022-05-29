import constants as c

class Card:
    '''This creates a cabo card.'''
    def __init__(self,name,val=0,abbrv=0,power=0) -> str:
        self.name = name
        self.value = val
        self.abbrv = abbrv
        self.power = power     


    def get_data(self):
        '''This returns the details of a specific card.'''
        print(f'{self.name},{self.value},{self.abbrv},{self.power}')

    def update_value(self):
        '''This function is used when building deck to update card values from constant.'''
        for key,value in c.CARD_VALUES.items():
            if self.name == key:
                self.value = value
    
    def update_abbrv(self):
        '''This function is used when building deck to update abbreviation values from constant.'''
        for key,value in c.CARD_ABBRV.items():
            if self.name == key:
                self.abbrv = value
    
    def update_powers(self):
        '''This function is used when building deck to update power values from constant.'''
        for key,value in c.CARD_POWERS.items():
            if self.name == key:
                self.power = value


    def get_power_string(self):
        '''This function returns the string related to the objects power.'''
        for key,value in c.POWERS.items():
            if self.power == value:
                return key

    
    def show_card(self):
        return self.name