# Ms. PacMan Agent

This is a reinforcement learning agent that plays Ms. PacMan through function
approximation.

This is a submission to the third assignment of McGill University's ECSE 526 -
Artificial Intelligence course. Details can be found
[here](http://www.cim.mcgill.ca/~jer/courses/ai/assignments/as3.html).

This agent has been able to score an average of over 4000 points each episode,
with a maximum recorded score of approximately 12500.

<img width="800" alt="screen shot 2016-11-14 at 13 29 37" src="https://cloud.githubusercontent.com/assets/723610/20955411/1ba33a42-bc11-11e6-86e4-fcfcf3240dfd.png">

# Setup

To run this, all one needs is Python 2.7 or above, the
`Arcade Learning Environment` with its Python bindings installed and
`opencv-python`.

If you're running this on OSX, you will also need `pygame` in order to display
the game screen.

# Running

To run, simply run:

```bash
python play.py
```

or

```bash
python play.py --help
```

for advanced options.

When running, you should see a window as pictured above (titled `ALE Viz`). The
`map` and `sliced map` windows would appear when running with the `--map-display`
option. The `map` window shows the reduced approximation of the game field,
whereas the `sliced map` window is the portion of the map the agent is currently
analyzing. A legend of the colors used in the maps is shown below:

Color   | Meaning
--------|--------
Blue    | Clear path
Orange  | Wall
White   | Pellet
Cyan    | Power-up
Magenta | Fruit
Red     | Bad ghost
Green   | Edible ghost
Yellow  | Ms. PacMan
