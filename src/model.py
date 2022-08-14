from __future__ import annotations

import random
from collections import deque
from time import sleep
from tokenize import String
from typing import Any, List, Optional
from xmlrpc.client import Boolean

from tabulate import tabulate

import constants as c
from view import *
import logging

logging.basicConfig(filename='log.log',
                    filemode='w',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(lineno)d %(message)s')


class Stack(deque):  # TODO need to refactor this to not inherit from deque?
    """Creates a hand and maintains functions related to a stack.
    Takes in a name string and a list of cards."""

    def __init__(self, name: str, members: List[Card]):
        self.members = members
        self.name = name

    def __str__(self):
        hand_list = []
        cards: Card
        for cards in self:
            card_name = cards.get_card_name()
            hand_list.append(card_name)
        return f"{self.name} contains {hand_list})"

    def get_pile_value(self) -> int:
        """Returns sum of the value of all cards in current stack."""
        return sum(c.value for c in self)

    def get_top_card(self) -> Card:
        """Returns the top card of the stack AKA card in index 0"""
        return self[0]


class Card:  # TODO add logic to show human hand vs. computer hand
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
        """Returns name attribute of Card"""
        return self.value

    def associate_value(self) -> bool:
        """This function is used when building deck
        to update card values from constant."""
        for key, value in c.CARD_VALUES.items():
            if self.name == key:
                self.value = value
        return True

    def associate_powers(self) -> bool:
        """This function is used when building deck to update power values from constant."""
        for key, value in c.CARD_POWERS_tester.items():
            if self.name == key:
                self.power = value
                return True
        return False

    def return_card_powers(self) -> str | None:
        """Returns value associated with the power defined in constants of the Card"""
        for key, value in c.POWERS.items():
            if self.power == value:
                power_value = key
                return power_value


class Game:

    def __init__(self,
                 human_pile,
                 computer_pile,
                 discard_pile,
                 deal_pile,
                 computer_pile_memory,
                 turn_count: int = 1,
                 open_hand: bool = False,
                 cabo_called: bool = False,
                 computer_difficulty: str = 'Easy'):
        self.open_hand: bool = open_hand  # set this to see every card in each hand each round
        self.human_pile: Stack = human_pile
        self.computer_pile: Stack = computer_pile
        self.discard_pile: Stack = discard_pile
        self.cabo_called: bool = cabo_called
        self.turn_count: int = turn_count
        self.deal_pile: Stack = deal_pile
        self.computer_pile_memory: Stack = computer_pile_memory
        self.name: str = ""
        self.computer_diff: str = computer_difficulty
        self.computer_opponent_memory = ["computer_opponent_memory"]

    def initialize_game(
            self
    ) -> None:  # TODO Enable use of player name and write instructions
        """Initial setup of game to gather human player information and show instructions."""
        Player1 = Player(present_intro(), 'Computer')

    def call_cabo_action(self) -> bool:
        """Sets cabo state evaluated in main game while loop"""
        self.cabo_called = True
        return True

    def discard_drawn_card(self) -> bool:
        """Transfers card from deal stack to discard stack"""
        make_transfer(self.deal_pile, self.discard_pile, 0, 0, True)
        return True

    def swap_drawn_card(
        self,
        pile_index: int,
        destination_pile,
    ) -> tuple[Stack, Stack]:
        """Enables a player to swap the "drawn" card with one in their pile
        and send the one in their pile to the discard pile.

        players_stack == players pile"""
        make_transfer(destination_pile, self.discard_pile, pile_index, 0)
        make_transfer(self.deal_pile, destination_pile, 0, pile_index)
        return destination_pile[0], self.discard_pile[0]

    def start_round(self) -> bool:
        """Displays initial information of round to human player."""
        present_round_spacer(self.turn_count)
        if self.open_hand == True:
            present_hand_table(self.computer_pile, True)
            present_hand_table(self.human_pile, True)
            sleep(2)  #TODO remove
            return True
        elif self.turn_count == 1 and self.open_hand == False:
            show_placeholder_hand(self.computer_pile)
            present_hand_table(self.human_pile)
            sleep(2)  #TODO remove
            return True
        else:
            show_placeholder_hand(self.computer_pile)
            show_placeholder_hand(self.human_pile)
            return True

    def start_human_turn(self):
        """Gather human turn input and triggers game play mechanics."""
        self.start_round()
        discard_card = self.discard_pile.get_top_card()
        swap_discard_card_response = present_swap_discard_prompt(discard_card)
        if swap_discard_card_response == 1:
            while True:
                try:
                    swap_card_destination_index: int = present_swap_card_prompt(
                    ) - 1
                    swap_results = swap(self.discard_pile, self.human_pile, 0,
                                        swap_card_destination_index)
                    present_swap_results(swap_results,
                                         swap_card_destination_index)
                except (IndexError, ValueError):
                    present_card_index_error()
                else:
                    break
            return True
        elif swap_discard_card_response == 0:
            while True:
                sleep(1)  # TODO remove this
                present_draw_card_preview(self.deal_pile[0])
                present_card_powers_string(self.deal_pile[0])
                turn_action_choice = present_action_prompt()
                try:
                    if turn_action_choice == 5:  # end game
                        exit()
                    elif turn_action_choice == 4:  # call cabo
                        if self.call_cabo_action() == True:
                            return present_cabo()
                    elif turn_action_choice == 3:
                        while True:
                            swap_card_destination_index: int = present_swap_card_prompt(
                            ) - 1
                            try:
                                swap_discard_card_response = self.swap_drawn_card(
                                    swap_card_destination_index,
                                    self.human_pile)
                                present_swap_draw_results(
                                    swap_discard_card_response,
                                    swap_card_destination_index)
                            except IndexError:
                                present_card_index_error()
                            else:
                                break
                        return True
                    elif turn_action_choice == 2:  # discard
                        self.discard_drawn_card()
                        sleep(3)
                        return True
                    elif turn_action_choice == 1:
                        drawn_card = get_drawn_card(self.deal_pile)
                        drawn_card_power = drawn_card.power
                        if drawn_card_power == 0:
                            raise ValueError
                        else:
                            use_power(drawn_card_power, self.human_pile,
                                      self.computer_pile)
                            return True
                    elif turn_action_choice > 6:
                        raise ValueError  # to make sure number is in range
                except ValueError:
                    if turn_action_choice == 2:
                        present_card_index_error()
                    if turn_action_choice == 1:
                        present_card_power_error()
                    else:
                        present_card_index_error()
                else:
                    break
            return True

    def computer_turn(self):  # TODO make this work lol
        self.start_round()
        self.computer_turn_discard_card_check()

        return

    def computer_turn_discard_card_check(self):
        '''Iterates through set of cards in current memory of computers pile, 
        and evaluates if the drawn card is of greater value. 
        If so, it replaces the card with the current discard card.
        
        Current strategy is too simplistic. Rewrite card memory to be list of tuples'''
        discard_card = self.discard_pile.get_top_card()
        upper_range: float = 1
        lower_range: float = .5

        def discard_calculation():
            if discard_card.get_card_value() >= 0:
                threshold = float(
                    (card.get_card_value() - discard_card.get_card_value()) /
                    card.get_card_value())
                logging.info(
                    f"1:discard card value is: {discard_card.get_card_value()} and threshold: {threshold} "
                )
            elif card.get_card_value() <= 0:
                threshold = 0
                logging.info(
                    f"2:discard card value is: {discard_card.get_card_value()} and threshold: {threshold} "
                )
            else:
                threshold = 1
                logging.info(
                    f"Else:discard card value is: {discard_card.get_card_value()} and threshold: {threshold} "
                )
            return threshold

        self.log_pile_state()

        for card in self.computer_pile_memory:
            if upper_range >= discard_calculation() >= lower_range:
                logging.info(
                    f"Discard card: {discard_calculation()} is between {upper_range} and {lower_range} - swapping."
                )
                swap_index = self.computer_pile_memory.index(card)
                logging.info(
                    f"Index of to be swapped card is {self.computer_pile_memory.index(card)}. This card is a {self.computer_pile[swap_index]}."
                )
                temporary_hold_for_swapped_card = self.computer_pile[swap_index]
                self.computer_pile_memory[
                    swap_index] = self.discard_pile.get_top_card()
                self.computer_pile[swap_index] = self.discard_pile.get_top_card(
                )
                self.discard_pile.appendleft(temporary_hold_for_swapped_card)
                logging.info(
                    f"Swapped {temporary_hold_for_swapped_card} at {swap_index} with a {self.computer_pile[swap_index]}"
                )
                logging.info(
                    f"Top card of discard pile is {self.discard_pile[0]}")
                break
        self.log_pile_state()

    def log_pile_state(self):
        logging.info(f"Top of deal pile is {str(self.deal_pile[0])}")
        logging.info(str(self.computer_pile))
        logging.info(str(self.computer_pile_memory))
        logging.info(str(self.discard_pile))
        logging.info(str(self.human_pile))

    def end_turn(self) -> bool:
        """Ends turn, increments turn count, and prints terminal indicator."""
        present_end_round(self.turn_count)
        self.turn_count_increment()
        return True

    def turn_count_increment(self) -> bool:
        """increments turn count indicator"""
        self.turn_count += 1
        return True


def build_deck() -> list[Card]:
    """Initial construction of the deck by creating cards defined in CARD_COUNTS_* and then iterating over them
    to update the value and power as defined in constants"""
    new_deck: list[Card] = []
    new_deck.extend(
        [Card(name) for name in c.CARD_COUNTS_4 for i in range(1, 5)])
    new_deck.extend(
        [Card(name) for name in c.CARD_COUNTS_2 for i in range(1, 3)])
    for card in new_deck:
        Card.associate_value(card)
    for card in new_deck:
        Card.associate_powers(card)
    return new_deck


def build_hand(source_stack: Stack, dest_stack: Stack) -> bool:
    """Creates initial hands for players with four cards"""
    n: int = 0
    while n < 4:
        make_transfer(source_stack, dest_stack, 0, n)
        n += 1
    return True


def transfer_action(source_stack: Stack,
                    dest_stack: Stack,
                    source_index: int = 0,
                    dest_index: int = 0,
                    describe: bool = False) -> tuple[str, str]:
    """***use Transfer()***
    Copies a card in one stack to destination stack with:
        - source stack as source_stack
        - destination stack as dest_stack
        - source_index  = source index to copy and delete card from.
        Default is "top" of deck or index 0
        - dest_index  = destination index to insert"""
    transfer_card: Card = source_stack[source_index]
    del source_stack[source_index]
    dest_stack.insert(dest_index, transfer_card)
    return transfer_card.name, dest_stack.name


def make_transfer(
    source_stack: Stack,
    dest_stack: Stack,
    source_index: int = 0,
    dest_index: int = 0,
    describe: bool = False,
) -> bool:
    """Copies a card in one stack to destination stack with:
    - source stack as source_stack
    - destination stack as dest_stack
    - source_index  = source index to copy and delete card from.
      Default is "top" of deck or index 0
    - dest_index  = destination index to insert

    Set 'describe' to True to print a record of the transfer to the terminal."""
    transfer_results = transfer_action(
        source_stack,
        dest_stack,
        source_index,
        dest_index,
    )
    if describe == True:
        present_transfer(transfer_results[0], transfer_results[1])
    return True


def swap(source_stack: Stack, dest_stack: Stack, source_index: int,
         dest_index: int) -> tuple[str, str]:
    """Switches Card from source_stack in source_index with Card in dest_stack to dest_index"""
    swap_card1: Card = source_stack[source_index]
    swap_card2: Card = dest_stack[dest_index]
    del source_stack[source_index]
    del dest_stack[dest_index]
    dest_stack.insert(dest_index, swap_card1)
    source_stack.insert(source_index, swap_card2)
    logging.info(
        f"Swapped {swap_card1} in {source_stack} for {swap_card2} in {dest_index}"
    )
    return swap_card1.name, swap_card2.name


def shuffle(stack_name: Stack) -> bool:
    """Shuffles cards of a Stack using random function."""
    rng = random.Random()
    rng.shuffle(stack_name)
    return True


def get_drawn_card(stack_name: Stack) -> Card:
    """Returns the draw card from the deal stack. Use this on the deal_stack due to bug where deal_stack can't be a Stack."""
    return stack_name[0]


def power_controller(drawn_card_power: int,
                     human_stack: Stack,
                     computer_stack: Stack,
                     destination_position: int | None = None,
                     source_position: int | None = None) -> tuple[Any, Any]:
    """Defines and triggers card power actions."""
    if source_position != None:
        source_index = (source_position) - 1
    if destination_position != None:
        destination_index = int(destination_position) - 1
    if drawn_card_power == 1:
        card_name = Card.get_card_name(human_stack[destination_index])
        return card_name, destination_position
    elif drawn_card_power == 2:
        card_name = Card.get_card_name(computer_stack[source_index])
        return card_name, source_position
    elif drawn_card_power == 3:
        swap(human_stack, computer_stack, source_index, destination_index)
    elif drawn_card_power == 4:
        swap_results = swap(human_stack, computer_stack, source_index,
                            destination_index)
        return swap_results


def use_power(drawn_card_power: int, source_pile: Stack,
              destination_pile: Stack) -> bool:
    """Collects necessary input from human to trigger correct card powers"""
    if (drawn_card_power == 1
       ):  # TODO rewrite to show revealed card with table rather than sentence
        peek_index = present_peek_self_prompt()
        card_name, index_n = power_controller(drawn_card_power, source_pile,
                                              destination_pile, peek_index)
        present_reveal_card(card_name, index_n)
        return True

    elif drawn_card_power == 2:
        peek_index = present_peek_card_prompt()
        card_name, index_n = power_controller(drawn_card_power, source_pile,
                                              destination_pile, None,
                                              peek_index)
        present_peek_card(card_name, index_n)
        return True

    elif drawn_card_power == 3:
        source_index, dest_index = present_blind_swap_prompt()
        r = power_controller(drawn_card_power, source_pile, destination_pile,
                             dest_index, source_index)
        present_blind_swap(source_index, dest_index)
        return True

    elif drawn_card_power == 4:
        source_index, dest_index = present_open_swap_prompt()
        r = power_controller(drawn_card_power, source_pile, destination_pile,
                             dest_index, source_index)
        c1 = r[0]
        c2 = r[1]
        present_open_swap(source_index, dest_index, c1, c2)
        return True
    else:
        return False


class Player:

    def __init__(self, name: str, type: str, difficulty: int):
        self.name = name
        self.type = type
        self.memory = {}
        self.difficulty = difficulty
