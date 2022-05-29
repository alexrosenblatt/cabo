import random
import constants as c

def build_deck() -> list:
    new_deck:list = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_powers(card) 
    return new_deck

def build_hand(deal_pile:str,human_deck:str):
        n: int
        n = 1 
        while n < 5:
            Stack.transfer(deal_pile,human_deck,0,n)
            n += 1

class Stack():
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self,members:str = []):
        self.members = members
    
    def shuffle(self):
        rng = random.Random()
        rng.shuffle(self)

    def remove(self,index: int ):
        self.members.pop(index)
        return True
    
    def add(self,index:int ,card):
        self.members.insert(index,card)
        return True

    def deal(self):
        return self.members.pop()
    
    def is_empty(self):
        return self.members == []

#add logic to show human hand vs. computer hand
    def show_hand(self):
        hand = []
        for cards in self:
            hand.append(cards.name)
        return print(f"Your hand contains: {hand}")
        
    def transfer(self_name:str,to_name:str,self_index:int,other_index:int):
        transfer_card = self_name[self_index]
        del(self_name[self_index])
        to_name.insert(other_index,transfer_card)    

class Card:
    '''This creates a cabo card.'''
    def __init__(self,name:str,val: int = 0,abbrv:str = '',power:int =0):
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
            







            
''' 
 #commenting out to test inheriting behaviors from the "list"  
    def __delitem__(self, indice):
        del self.members[indice]

# stolen from pycarddealer

    def __getitem__(self, key):
        self_len = len(self)
        if isinstance(key, slice):
            return [self[i] for i in xrange(*key.indices(self_len))]
        elif isinstance(key, int):
            if key < 0 :
                key += self_len
            if key >= self_len:
                raise IndexError("The index ({}) is out of range.".format(key))
            return self.members[key]
        else:
            raise TypeError("Invalid argument type.")
    
    def __len__(self):
        """
        Allows check the Stack length, with len.
        :returns:
            The length of the stack (self.members).
        """
        return len(self.members)
'''  