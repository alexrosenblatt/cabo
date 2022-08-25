from __future__ import annotations

import random
from collections import deque
from time import sleep

from typing import Any, Tuple, TypedDict

from tabulate import tabulate

import constants as c
from view import *
import logging

from attrs import define

from view import present_other_player_card_discard

logging.basicConfig(filename='log.log',
                    filemode='w',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(lineno)d %(message)s')


class CardMemory(TypedDict):
    stack_name: str
    index: int
    card: Card
    value: int


class Player:

    def __init__(self, name: str, type: int, difficulty: int | None = None):
        self.name = name
        self.type = type
        self.pile: Pile = Pile(self)
        self.difficulty = difficulty
        self.memory: list[CardMemory] = []
        if type == 1:
            self.ai = ComputerAI((1, 1))

    def insert_in_hand_and_memorize(self, index, object: Card, blind=True):
        self.pile.insert(index, object)
        if not blind:
            self.memory.insert(
                0, {
                    'stack_name': self.name,
                    'index': index,
                    'card': object,
                    'value': object.value
                })

    def _start_game_memorize(self):
        for card in self.pile:
            index = self.pile.index(card)
            object: Card = card
            self.memory.insert(
                0, {
                    'stack_name': self.name,
                    'index': index,
                    'card': object,
                    'value': object.value
                })
            if self.pile.index(card) >= 1:
                break

    def get_current_hand_value(self):
        current_hand_value = 0
        for card in self.memory:
            current_hand_value += int(card['value'])
        return current_hand_value


class Pile(deque):
    """Creates a hand and maintains functions related to a pile of cards.
    Takes in a name string and a list of cards."""

    def __init__(self, owner=None, name: str = ''):
        self.owner = owner
        if self.owner:
            self.name = self.owner.name
        else:
            self.name = name

    def __repr__(self):
        hand_list = []
        cards: Card
        for cards in self:
            card_name = cards.get_card_name()
            hand_list.append(card_name)
        return f"{self.name} contains {hand_list})"

    def get_sum_value(self) -> int:
        """Returns sum of the value of all cards in current stack."""
        return sum(c.value for c in self)

    def get_top_card(self) -> Card:
        """Returns the top card of the stack AKA card in index 0"""
        return self[0]


class Card:
    """This creates a cabo card."""

    def __init__(self, name: str, value: int = 0, power: int = 0):
        self.name = name
        self.value = value
        self.power = power

    def __str__(self):
        return self.name

    def get_card_name(self) -> str:
        """Returns name attribute of Card"""
        return self.name

    def get_card_value(self) -> int:
        """Returns value attribute of Card"""
        return self.value

    def get_card_powers(self) -> str | None:
        """Returns value associated with the power defined in constants of the Card"""
        for key, value in c.POWERS.items():
            if self.power == value:
                power_value = key
                return power_value

    def _associate_value(self) -> bool:
        """This function is used when building deck
        to update card values from constant."""
        for key, value in c.CARD_VALUES.items():
            if self.name == key:
                self.value = value
        return True

    def _associate_powers(self) -> bool:
        """This function is used when building deck to update power values from constant."""
        for key, value in c.CARD_POWERS_tester.items():
            if self.name == key:
                self.power = value
                return True
        return False


class Game:

    def __init__(self,
                 turn_count: int = 1,
                 open_hand: bool = False,
                 cabo_called: bool = False,
                 computer_difficulty: str = 'Easy'):

        self.player_list: list[Player] = []
        self.discard_pile = Pile(name='discard_pile')
        self.deal_pile = Pile(name='deal_pile')

        self.computer_difficulty: str = computer_difficulty

        self.turn_count: int = turn_count
        self.cabo_called: bool = cabo_called
        self.is_open_hand: bool = open_hand  # set this to see every card in each hand each round

    def _create_players(self, human_count, computer_count):
        count = 0
        for _ in range(human_count):
            self.player_list.append(Player(f"human_{count}", 0))
            count += 1
        count = 0
        for _ in range(computer_count):
            self.player_list.append(Player(f"computer_{count}", 1))
            count += 1

    def initialize_game(self) -> None:
        """Initial setup of game to gather human player information and show instructions."""
        (human_player_count,
         computer_player_count) = present_game_start_prompt()
        self._create_players(human_player_count, computer_player_count)
        deal_pile = self._build_deck()
        random.shuffle(deal_pile)
        for cards in deal_pile:
            self.deal_pile.append(cards)
        transfer(self.deal_pile, self.discard_pile, 0, 0)
        for player in self.player_list:
            self._build_hand(self.deal_pile, player.pile)
            player._start_game_memorize()

    def _build_deck(self) -> list[Card]:
        """Initial construction of the deck by creating cards defined in CARD_COUNTS_* and then iterating over them
        to update the value and power as defined in constants"""
        new_deck: list[Card] = []
        new_deck.extend(
            [Card(name) for name in c.CARD_COUNTS_4 for i in range(1, 5)])
        new_deck.extend(
            [Card(name) for name in c.CARD_COUNTS_2 for i in range(1, 3)])
        for card in new_deck:
            Card._associate_value(card)
        for card in new_deck:
            Card._associate_powers(card)
        return new_deck

    def _build_hand(self, source_stack: Pile, dest_stack: Pile) -> bool:
        """Creates initial hands for players with four cards"""
        n: int = 0
        while n < 4:
            transfer(source_stack, dest_stack, 0, n)
            n += 1
        return True

    def set_cabo_state(self) -> bool:
        """Sets cabo state evaluated in main game while loop"""
        self.cabo_called = True
        return True

    def discard_drawn_card(self) -> bool:
        """Transfers card from deal stack to discard stack"""
        transfer(self.deal_pile, self.discard_pile, 0, 0, True)
        return True

    def start_round(self) -> bool:
        """Displays initial information of round to human player."""
        present_round_spacer(self.turn_count)
        if self.is_open_hand == True:
            for player in self.player_list:
                present_hand_table(player.pile, True)
            sleep(2)  #TODO remove
            return True
        elif self.turn_count == 1 and self.is_open_hand == False:
            for player in self.player_list:
                if player.type == 1:
                    show_placeholder_hand(player.pile)
                else:
                    present_hand_table(player.pile)
            sleep(2)  #TODO remove
            return True
        else:
            for player in self.player_list:
                show_placeholder_hand(player.pile)
        return True

    def start_turn(self, player: Player):
        self.start_round()
        current_players_pile = player.pile
        current_player_type = player.type
        drawn_discard_card = self.discard_pile.get_top_card()
        discard_card_swapped = self.evaluate_and_action_discard_card(
            current_player_type, current_players_pile, drawn_discard_card,
            player)
        if not discard_card_swapped:
            turn_action_choice = self.evaluate_drawn_card(
                player, current_player_type)
            try:
                if turn_action_choice == 5:  # end game
                    exit()
                elif turn_action_choice == 4:  # call cabo
                    if self.set_cabo_state():
                        return present_cabo()
                elif turn_action_choice == 3:
                    self.swap_drawn_card(current_player_type,
                                         current_players_pile, player)
                    return True
                elif turn_action_choice == 2:  # discard
                    self.discard_drawn_card()
                    return True
                elif turn_action_choice == 1:
                    self.use_power_on_card(current_player_type,
                                           current_players_pile, player)
                    return True
                else:
                    raise ValueError  # to make sure number is in range
            except ValueError:
                if turn_action_choice == 2:
                    present_card_index_error()
                if turn_action_choice == 1:
                    present_card_power_error()
                else:
                    present_card_index_error()

    def use_power_on_card(self, current_player_type, current_players_pile,
                          player):
        drawn_card = get_drawn_card(self.deal_pile)
        drawn_card_power = drawn_card.power
        if drawn_card_power == 0:
            raise ValueError
        else:
            if not drawn_card_power == 1:
                target_players_pile = self.get_opponent_choice(
                    current_player_type, current_players_pile, player)
                self.use_power(drawn_card_power, current_players_pile,
                               target_players_pile, current_player_type, player)
            else:
                target_players_pile = self.player_list[1].pile
                self.use_power(drawn_card_power, current_players_pile,
                               target_players_pile, current_player_type, player)

    def log_pile_state(self):

        logging.info(f"Top of deal pile is {str(self.deal_pile[0])}")
        for player in self.player_list:
            logging.info(str(player.pile))
            logging.info(str(player.memory))
        logging.info(str(self.discard_pile))

    def end_turn(self) -> bool:
        """Ends turn, increments turn count, and prints terminal indicator."""
        present_end_round(self.turn_count)
        self.turn_count_increment()
        return True

    def turn_count_increment(self) -> bool:
        """increments turn count indicator"""
        self.turn_count += 1
        return True

    def evaluate_and_action_discard_card(self, current_player_type,
                                         current_players_pile, top_discard_card,
                                         player: Player):
        if current_player_type == 0:
            response = present_swap_discard_prompt(top_discard_card)
        else:
            response = self.get_computer_discard_evaluation(
                top_discard_card, current_players_pile)
        if response == 1:
            while True:
                try:
                    if current_player_type == 0:
                        swap_card_destination_index = present_swap_card_prompt(
                        ) - 1
                    elif current_player_type == 1:
                        swap_card_destination_index = player.ai.get_computer_swap_card_index(
                        )
                    else:
                        break
                except (IndexError, ValueError):
                    present_card_index_error()
                finally:
                    swap_results = swap(self.discard_pile,
                                        current_players_pile,
                                        0,
                                        swap_card_destination_index,
                                        is_blind=False)
                    present_swap_results(swap_results,
                                         swap_card_destination_index)
                return True
        elif response == 0:
            return False

    def swap_drawn_card(self, current_player_type, current_players_pile,
                        player):
        while True:
            try:
                if current_player_type == 0:
                    swap_card_destination_index = present_swap_card_prompt() - 1
                else:
                    swap_card_destination_index = player.ai.get_computer_drawn_card_index(
                    )
                swap_discard_card_response = swap(self.deal_pile,
                                                  current_players_pile,
                                                  0,
                                                  swap_card_destination_index,
                                                  is_blind=False)
                present_swap_draw_results(swap_discard_card_response,
                                          swap_card_destination_index)
            except IndexError:
                present_card_index_error()
            else:
                break

    def get_opponent_choice(self, current_player_type, current_players_pile,
                            player):
        player_list = self.player_list
        if len(player_list) > 2:
            if current_player_type == 0:
                choice_response = int(
                    present_player_choice(player_list, current_players_pile))
                return self.player_list[choice_response].pile

            else:
                return player.ai.get_computer_opponent_choice_for_power(
                    player_list)
        else:
            return player_list[1].pile

    def evaluate_drawn_card(self, player: Player, current_players_type):
        drawn_card = self.deal_pile.get_top_card()
        if current_players_type == 0:
            present_draw_card_preview(drawn_card)
            present_card_powers_string(drawn_card)
            turn_action_choice = present_action_prompt()
        else:
            turn_action_choice = player.ai.get_computer_action_choice(
                drawn_card)
        return turn_action_choice

    def use_power(self, drawn_card_power: int, current_player_pile: Pile,
                  target_player_pile: Pile, current_player_type,
                  player) -> bool:
        """Collects necessary input from human to trigger correct card powers"""
        if drawn_card_power == 1:
            if current_player_type == 0:
                peek_index = present_peek_self_prompt()
            else:
                peek_index = player.ai.get_computer_self_peek_index()
            card_name = Card.get_card_name(current_player_pile[peek_index])
            present_reveal_card(card_name, peek_index)
            return True

        elif drawn_card_power == 2:
            if current_player_type == 0:
                peek_index = present_peek_card_prompt()
            else:
                peek_index = player.ai.get_computer_peek_index()
            card_name = Card.get_card_name(target_player_pile[peek_index])
            present_peek_card(card_name, peek_index)
            return True

        elif drawn_card_power == 3:
            if current_player_type == 0:
                source_index, destination_index = present_swap_prompt()
            else:
                source_index, destination_index = player.ai.get_computer_swap_choice(
                )
            swap(current_player_pile,
                 target_player_pile,
                 source_index,
                 destination_index,
                 is_blind=True)
            if current_player_type == 0:
                present_blind_swap(source_index, destination_index)
            else:
                return True
            return True

        elif drawn_card_power == 4:
            if current_player_type == 0:
                source_index, destination_index = present_swap_prompt()
            else:
                source_index, destination_index = player.ai.get_computer_swap_choice(
                )
            card_1, card_2 = swap(current_player_pile,
                                  target_player_pile,
                                  source_index,
                                  destination_index,
                                  is_blind=False)
            present_open_swap(source_index, destination_index, card_1, card_2)
            return True
        else:
            return False

    def get_computer_discard_evaluation(self, top_discard_card,
                                        current_players_pile):
        '''Iterates through set of cards in current memory of computers pile, 
        and evaluates if the drawn card is of greater value. 
        If so, it replaces the card with the current discard card.
        
        Current strategy is too simplistic. Rewrite card memory to be list of tuples'''
        player: Player = current_players_pile.owner

        upper_range: float = 1
        lower_range: float = .5

        def computer_discard_calculation():
            discard_card_value = top_discard_card.get_card_value()
            memorized_card_value = memorized_card.get('card').value
            if discard_card_value > 0 and memorized_card_value > 0:
                threshold = float((memorized_card_value - discard_card_value) /
                                  memorized_card_value)
                logging.info(
                    f"1:discard card value is: {discard_card_value} and threshold: {threshold} "
                )
            elif memorized_card.get('value') <= 0:
                threshold = 0
                logging.info(
                    f"2:discard card value is: {discard_card_value} and threshold: {threshold} "
                )
            else:
                threshold = 1
                logging.info(
                    f"Else:discard card value is: {discard_card_value} and threshold: {threshold} "
                )
            return threshold

        player.memory.sort(key=lambda x: x['value'], reverse=True)
        print(player.memory)
        for memorized_card in player.memory:
            if upper_range >= computer_discard_calculation() >= lower_range:
                # logging.info(
                #     f"Discard card: {computer_discard_calculation()} is between {upper_range} and {lower_range} - swapping."
                # )
                # logging.info(
                #     f"Index of to be swapped card is {player.memory.index(memorized_card)}. This card is a {player.memory[swap_index].card.name}."
                # )
                # logging.info(
                #     f"Top card of discard pile is {self.discard_pile[0]}")
                return 1
            else:
                return 0


@define
class ComputerAI:
    difficulty: Tuple

    def get_computer_swap_card_index(self):
        return 1

    def get_computer_action_choice(self, drawn_card):
        return 1

    def get_computer_drawn_card_index(self):
        return 1

    def get_computer_opponent_choice_for_power(self, player_list) -> Pile:
        return player_list[1].pile

    def get_computer_self_peek_index(self) -> int:
        return 1

    def get_computer_peek_index(self) -> int:
        return 1

    def get_computer_swap_choice(self) -> tuple[int, int]:
        source_index = 1
        destination_index = 1
        return source_index, destination_index


def transfer(source_pile: Pile,
             destination_pile: Pile,
             source_index: int = 0,
             dest_index: int = 0,
             describe: bool = False) -> bool:
    """Copies a card in one stack to destination stack with:
    - source stack as source_stack
    - destination stack as dest_stack
    - source_index  = source index to copy and delete card from.
      Default is "top" of deck or index 0
    - dest_index  = destination index to insert

    Set 'describe' to True to print a record of the transfer to the terminal."""
    transfer_card = source_pile[source_index]
    del source_pile[source_index]
    destination_pile.insert(dest_index, transfer_card)
    if describe == True:
        present_transfer(transfer_card.name, destination_pile.name)
    return True


def swap(source_pile: Pile,
         destination_pile: Pile,
         source_index: int,
         dest_index: int,
         is_blind=False) -> tuple[Card, Card]:
    """Switches Card from source_stack at source_index with Card in dest_stack at dest_index"""
    swap_card1: Card = source_pile[source_index]
    swap_card2: Card = destination_pile[dest_index]
    del source_pile[source_index]
    del destination_pile[dest_index]
    insert_and_memorize(destination_pile, dest_index, swap_card1,
                        destination_pile.owner, is_blind)
    insert_and_memorize(source_pile, source_index, swap_card1,
                        destination_pile.owner, is_blind)
    log_swap_results(source_pile, source_index, destination_pile, dest_index,
                     swap_card1, swap_card2)
    return swap_card1, swap_card2


def insert_and_memorize(pile,
                        index,
                        object: Card,
                        player_taking_action,
                        is_public=False,
                        is_blind=False):
    pile.insert(index, object)
    if is_blind:
        player_taking_action.memory.insert(0, {
            'stack_name': pile.name,
            'index': index,
            'card': object,
        })
    if not is_public:
        present_other_player_card_discard(pile, index, object,
                                          player_taking_action)
    else:
        pass


def shuffle(pile_name: Pile) -> Pile:
    """Shuffles cards of a Stack using random function."""
    rng = random.Random()
    rng.shuffle(pile_name)
    return pile_name


def get_drawn_card(pile_name: Pile) -> Card:
    """Returns the draw card from the deal stack. Use this on the deal_stack due to bug where deal_stack can't be a Stack."""
    return pile_name[0]


def log_swap_results(source_pile, source_index, destination_pile,
                     destination_index, swap_card1, swap_card2):
    logging.info(
        f"Swapped {swap_card1} in {source_pile}'s hand at index:{source_index} for {swap_card2} at {destination_index} in {destination_pile}"
    )
