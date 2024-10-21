import math
import secrets

from ursina import Vec3, color

from org.odds.lang.lang import phrases
from org.odds.lang.lexical import normalize_str, plots_3d
from org.odds.game.pim.quantum import QuantumRealm


def preprocess_for_3d(s: str):
    normalized = normalize_str(s)
    # map each value to a whole number (decimal values don't work well in ursina plots
    normalized = [math.floor(w * 10) for w in normalized]

    plotted = plots_3d(normalized)
    # need to treat plots, so that each coordinate becomes a 3D vectorwad
    # map each coordinate to Vec3
    plotted = [Vec3(tuple(x)) for x in plotted]

    return plotted


def main():
    q = QuantumRealm()

    color_bunch = [color.green, color.red, color.blue, color.white, color.orange, color.pink, color.magenta]
    [q.add_plot(preprocess_for_3d(s), the_color=secrets.choice(color_bunch)) for s in phrases['long_sentences']]

    q.app.run()


if __name__ == "__main__":
    main()
