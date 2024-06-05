import math
import secrets

from ursina import Vec3, color

from lang import plots_3d, normalize_str, phrases
from org.odds.game.pim.quantum import QuantumRealm


def preprocess_for_3d(s: str):
    normalized = normalize_str(s)
    # map each value to a whole number (decimal values don't work well in ursina plots
    normalized = [math.floor(w * 10) for w in normalized]

    plotted = plots_3d(normalized)
    # need to treat plots, so that each coordinate becomes a 3D vector
    # map each coordinate to Vec3
    plotted = [Vec3(tuple(x)) for x in plotted]

    return plotted


def main():
    q = QuantumRealm()
    # q.add_plot([(1, 0, 1), (1, 2, 2), (4, 1, 1), (2, 1, 0)])
    # sent = secrets.choice(phrases['long_sentences'])

    # plot_sent = preprocess_for_3d(sent)
    color_bunch = [color.green, color.red, color.blue, color.white, color.orange, color.pink, color.magenta]
    [q.add_plot(preprocess_for_3d(s), the_color=secrets.choice(color_bunch)) for s in phrases['long_sentences']]

    # q.add_plot(plot_sent)
    q.app.run()


if __name__ == "__main__":
    main()
