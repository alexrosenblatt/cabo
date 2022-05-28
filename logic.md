# Cabo Logic
## Setup
### Card Powers
 
- 7: look at own card
- 8: look at own card
- 9: look at others card
- 10: look at others card
- Q: blind swap
- j: blind swap
- black king: look at other players card and decide whether to swap for your own
## Scoring
A = 1 
2-10: face-value
J = 11
Q = 12
K = 13
rK = -1
Jokers = 0 
## Turn Mechanics
### Normal Turn
- Decide whether to say Cabo
- Look at faceup card 
    - If face up card matchs any known card:
        - Burn
            - If it's your own card, then remove card
            - If it's someone elses card, give them highest known card or random card
    - If desired, pick up card and swap with one of your four cards
    - If not, draw card
        - If power use power, unless x
        - If no power and value < x
        - if no power and over x, discard

