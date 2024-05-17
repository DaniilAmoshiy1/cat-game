# This is my project "cat-game"

## Only for PC or laptop.

## What needs from hardware and software for interacting with code:

Keyboard, mouse, and random IDE

## A little about the project:

In this game there are only three files that are responsible for the game,\
there is no special logic in the game, first the loading screen starts,\
and then the game background and the player (cat), you can just walk\
in the game. There is also music here, it is possible to control it.

### Controls:
The cat walks using the W, A, S, D keys.\
You can switch music through buttons **right** and **left**\
You can exit the game by simply closing the window or pressing the **Esc** key.

### Files:

Main startup file "main.py"\
The file "game.py" contains the game class itself\
Also file "constants.py" for constants in project


## Unfortunately, my project is not accessible through the site, the server is not up. You can check how working code through git clone.

## Now let's look at the command line commands:

### deploy virtual environment

```bash
python -m venv venv
```

Activation for **windows**:

```bash
venv/scripts/activate
```

### install libraries

```bash
pip install -r requirements.txt
```

### run pygame

```bash
python game/main.py
```

### build html

```bash
pygbag --build game
```
