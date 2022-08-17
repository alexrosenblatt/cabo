from typing import Dict


class Card():

    def __init__(self, card_value) -> None:
        self.card_value = card_value

    def __repr__(self) -> str:
        return f"{self.card_value}"


class Player():

    def __init__(self, player_name) -> None:
        self.player_name = player_name
        self.player_memory = []
        self.pile: list[Card] = []

    def __repr__(self) -> str:
        return f"{self.pile}"
        pass


class Game():

    def __init__(self, human_count, computer_count) -> None:
        self.discard_pile: list[Card] = [Card(3)]
        self.draw_pile: list[Card] = []
        self.player_list = []
        self._create_players(human_count, computer_count)

    def _create_players(self, human_count, computer_count):
        count = 0
        for _ in range(human_count):
            self.player_list.append(Player(f"human_{count}"))
            count += 1
        count = 0
        for _ in range(computer_count):
            self.player_list.append(Player(f"computer_{count}"))
            count += 1

    def setup_game(self):
        for player in self.player_list:
            self.build_hand(1, 5, player.pile)
        [self.build_hand(1, 10, self.draw_pile) for _ in range(2)]

    def build_hand(self, min, max, pile):
        for n in range(min, max):
            new_card = Card(n)
            pile.append(new_card)

    def get_top_discard_card(self) -> Card:
        drawn_card = self.discard_pile[0]
        return drawn_card

    def get_top_draw_card(self) -> Card:
        drawn_card = self.draw_pile[0]
        return drawn_card

    def discard_card(self, discarded_card) -> None:
        self.discard_pile.insert(0, discarded_card)

    def _swap_card(self, source_pile: list[Card], destination_pile: list[Card],
                   source_index: int, destination_index: int):
        source_pile[source_index], destination_pile[
            destination_index] = destination_pile[
                destination_index], source_pile[source_index]

    def _burn_card(self, source_pile, destination_pile, source_index,
                   destination_index):
        if source_pile[source_index].card_value == destination_pile[
                destination_index].card_value:
            burnt_card = source_pile.pop(source_index)
            self.discard_card(burnt_card)
            return True
        else:
            return False

    def burn_own_card_with_discard_card(self, source_index):
        if self._burn_card(self.player_list[0].pile, self.discard_pile,
                           source_index, 0):
            self.player_list[0].pile.insert(source_index, 'x')
        else:
            self.player_list[0].pile.insert(0, self.get_top_draw_card())

    def burn_other_player_card_with_discard(self, source_index,
                                            destination_index):
        if self._burn_card(self.player_list[1].pile, self.discard_pile,
                           source_index, destination_index):
            self.player_list[1].pile.insert(source_index, Card('x'))
            self.player_list[1].pile.append(self.player_list[0][0])
            self.player_list[0].pile.insert(0, Card('x'))
        else:
            self.player_list[0].pile.insert(0, self.get_top_draw_card())


def print_currentstate():
    for player in g.player_list:
        print(f"{player.player_name}:{player.pile}")
    print(f"discard pile: {g.discard_pile}")
    print(f"draw pile: {g.draw_pile}")


g = Game(1, 1)
g.setup_game()
print(g.get_top_draw_card())
g.burn_own_card_with_discard_card(2)
