# Flappy Bird with NEAT AI

This project is a Flappy Bird clone built with Python and Pygame, featuring both a player-controlled mode and an AI mode powered by the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Features

- **Player Mode:** Control the bird manually using the spacebar or a joystick button.
- **AI Mode:** Train an AI to play Flappy Bird using NEAT.
- **Joystick Support:** Play with a connected game controller.

Player|AI
--|--
<video src="https://github.com/user-attachments/assets/cf74cb9a-773d-4f67-be27-abba9ac287ab" />|<video src="https://github.com/user-attachments/assets/46caea81-3066-4ca3-8dd2-e25168c01e0d"/>


## Installation

1. Clone the repository:

```sh
git clone https://github.com/RezaTaheri01/flappy-bird-ai.git
cd flappy-bird-ai
```

2. Install the required packages:

```sh
pip install pygame neat-python
```

3. Set up the project structure:

```
flappy-bird-neat/
├── assets/
│   └── imgs/
├── src/
│   ├── base.py
│   ├── birds.py
│   └── pipe.py
├── config-feedforward.txt
└── main.py
```

## How to Run

- **Player Mode:**

In `src/constants.py`, set `PLAYER_MODE` to `True`:

```python
PLAYER_MODE = True
```

Then run the game:

```sh
python main.py
```

- **AI Mode:**

Set `PLAYER_MODE` to `False`:

```python
PLAYER_MODE = False
```

Run the NEAT training:

```sh
python main.py
```

## Controls

- **Spacebar / Controller A Button:** Make the bird jump
- **ESC:** Quit the game

## NEAT Configuration

The NEAT algorithm's settings are in the `config-feedforward.txt` file. You can tweak parameters like population size, mutation rates, and more to optimize training.

## Saving the Best Model

When the AI reaches a specific score(defined in src/constants.py), the best-performing neural network is saved as `best.pickle`.

## Acknowledgments

- Pygame for game development
- NEAT-Python for neural evolution

## Assets and Source Code Links:
- [sourabhv/FlapPyBird](https://github.com/LeonMarqs/Flappy-bird-python)
- [techwithtim](https://github.com/techwithtim/NEAT-Flappy-Bird)

---

Enjoy playing (or watching) Flappy Bird! 🐦

