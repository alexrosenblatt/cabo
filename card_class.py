import constants as c

class Card:
    '''This creates a cabo card.'''
    def __init__(self,val,abbrv,power) -> None:
        self.value = val
        self.abbrv = abbrv
        self.power = power        
    
    def get_data(self):
        print(f'{self.value},{self.abbrv},{self.power}')

    def power_string(self):
        for key,value in c.POWERS.items():
            if self.power == value:
                return key



ace = Card(12,12,4)

ace.get_data()
print(ace.power_string())

