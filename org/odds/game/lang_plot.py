import math
import secrets

from ursina import Vec3

from lang import plots_3d, normalize_str, phrases
from org.odds.game.pim.quantum import QuantumRealm

def main():
    q = QuantumRealm()
    # q.add_plot([(1, 0, 1), (1, 2, 2), (4, 1, 1), (2, 1, 0)])
    sent = secrets.choice(phrases['long_sentences'])
    normal_sent = normalize_str(sent)
    normal_sent = [math.floor(w * 10) for w in normal_sent]
    plot_sent = plots_3d(normal_sent)
    # need to treat plot_3d list so that each coordinate becomes a 3D vector (Vec3)
    plot_sent = [Vec3(tuple(x)) for x in plot_sent]

    q.add_plot(plot_sent)
    q.app.run()


if __name__ == "__main__":
    main()
