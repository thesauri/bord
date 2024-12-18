# Bord

Bord is a chair and table collecting game intended for bot tournaments.
The goal is simple: collect as many chairs and tables as possible.

## Setup

1. Install Python 3.8 or later
2. Install [Pyxel](https://github.com/kitao/pyxel)
3. Clone this repository
4. Run `pyxel bord.py`

## Creating your own bot

1. Copy [bots/dumbster_bot.py](bots/dumbster_bot.py) and rename it
2. Implement the `get_action` method in the Bot class
3. Initialize your bot in the `__init__` method of the Game class in [bord.py](bord.py)
