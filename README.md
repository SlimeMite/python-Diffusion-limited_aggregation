# DLA Probability Calculation

The important part of this repo is the algorithm for calculating the probabilities for where the new Tile could end up going. The approach scales quite well and could be cached for faster usage in the future, greatly accelerating generation of large Patterns, without sacrificing any accuracy compared to calculating it normally. Going in reverse would be very useful, but I haven't figured out how to do that yet.

All important Logic is in the marcher.py file.

Start the window_interactive.py file to use the gui.

No research was done on how DLA actually works, so there's probably a better way.
All Knowledge comes from this awesome video: [https://www.youtube.com/watch?v=gsJHzBTPG0Y](https://www.youtube.com/watch?v=gsJHzBTPG0Y)

