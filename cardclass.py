import constants as c

class Card:
    '''This creates a cabo card.'''
    def __init__(self,name,val=0,abbrv=0,power=0) -> None:
        self.name = name
        self.value = val
        self.abbrv = abbrv
        self.power = power        
    
    def get_data(self):
        print(f'{self.name},{self.value},{self.abbrv},{self.power}')

    def get_power_string(self):
        for key,value in c.POWERS.items():
            if self.power == value:
                return key

    def update_value(self):
        for key,value in c.CARD_VALUES.items():
            if self.name == key:
                self.value = value
    
    def update_abbrv(self):
        for key,value in c.CARD_ABBRV.items():
            if self.name == key:
                self.abbrv = value
    
    def update_powers(self):
        for key,value in c.CARD_POWERS.items():
            if self.name == key:
                self.power = value

