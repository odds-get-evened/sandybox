import os.path
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans, DBSCAN
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KDTree
from verble.lexicon import LexicalAnalyzer, normalize_arr, normalize_str, plots_2d, plots_3d

PHRASES = [
    "The ship ran before a fresh North wind till we had reached the sea that lies between Crete and Libya; there, "
    "however, Jove counselled their destruction, for as soon as we were well out from Crete and could see nothing but "
    "sea and sky, he raised a black cloud over our ship and the sea grew dark beneath it. Then Jove let fly with his "
    "thunderbolts and the ship went round and round and was filled with fire and brimstone as the lightning struck "
    "it. The men fell all into the sea; they were carried about in the water round the ship looking like so many "
    "sea-gulls, but the god presently deprived them of all chance of getting home again. I was all dismayed. Jove, "
    "however, sent the ship’s mast within my reach, which saved my life, for I clung to it, and drifted before the "
    "fury of the gale. Nine days did I drift but in the darkness of the tenth night a great wave bore me on to the "
    "Thesprotian coast. There Pheidon king of the Thesprotians entertained me hospitably without charging me anything "
    "at all—for his son found me when I was nearly dead with cold and fatigue, whereon he raised me by the hand, "
    "took me to his father’s house and gave me clothes to wear. There it was that I heard news of Ulysses, "
    "for the king told me he had entertained him, and shown him much hospitality while he was on his homeward "
    "journey. He showed me also the treasure of gold, and wrought iron that Ulysses had got together. There was "
    "enough to keep his family for ten generations, so much had he left in the house of king Pheidon. But the king "
    "said Ulysses had gone to Dodona that he might learn Jove’s mind from the god’s high oak tree, and know whether "
    "after so long an absence he should return to Ithaca openly, or in secret. Moreover the king swore in my "
    "presence, making drink-offerings in his own house as he did so, that the ship was by the water side, "
    "and the crew found, that should take him to his own country. He sent me off however before Ulysses returned, "
    "for there happened to be a Thesprotian ship sailing for the wheat-growing island of Dulichium, and he told those "
    "in charge of her to be sure and take me safely to King Acastus."
    "As she sat watching the world go by, something caught her eye. It wasn't so much its color or shape, but the way it was moving. She squinted to see if she could better understand what it was and where it was going, but it didn't help. As she continued to stare into the distance, she didn't understand why this uneasiness was building inside her body. She felt like she should get up and run. If only she could make out what it was. At that moment, she comprehended what it was and where it was heading, and she knew her life would never be the same.",
    "It was going to rain. The weather forecast didn't say that, but the steel plate in his hip did. He had learned over the years to trust his hip over the weatherman. It was going to rain, so he better get outside and prepare.",
    "There was something special about this little creature. Donna couldn't quite pinpoint what it was, but she knew with all her heart that it was true. It wasn't a matter of if she was going to try and save it, but a matter of how she was going to save it. She went back to the car to get a blanket and when she returned the creature was gone.",
    "It went through such rapid contortions that the little bear was forced to change his hold on it so many times he became confused in the darkness, and could not, for the life of him, tell whether he held the sheep right side up, or upside down. But that point was decided for him a moment later by the animal itself, who, with a sudden twist, jabbed its horns so hard into his lowest ribs that he gave a grunt of anger and disgust.",
    "Hopes and dreams were dashed that day. It should have been expected, but it still came as a shock. The warning signs had been ignored in favor of the possibility, however remote, that it could actually happen. That possibility had grown from hope to an undeniable belief it must be destiny. That was until it wasn't and the hopes and dreams came crashing down."
]

MODEL_STORAGE_PATH = Path(os.path.expanduser('~'), '.databox', 'word-machine')


def smallest_divisor_greater_than(n, greater_than=1):
    for i in range(greater_than + 1, n + 1):
        if n % i == 0:
            return i

    return n


def split_list_fit(ls: list, row_len=None, greater_than=1, pad_value=0.0):
    # get length of the list
    ls_len = len(ls)

    # if no row_len is provided use smallest divisor greater than 1
    if row_len is None:
        row_len = smallest_divisor_greater_than(ls_len, greater_than)
    else:
        # check if provided row length is valid, otherwise adjust with padding
        if row_len < 2:
            raise ValueError('row length must be greater than 1')

    # calculate how much to pad
    remainder = ls_len % row_len
    if remainder != 0:
        # add pad_value to the list length, where it is divisible by row_len
        pads = [pad_value] * (row_len - remainder)
        ls += pads

    # split the list up
    return [
        ls[i:i + row_len] for i
        in range(0, len(ls), row_len)
    ]


def plot_sphere(xx, center, radius, color):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    xx.plot_surface(x, y, z, color=color, alpha=0.1)


def word_mechanism(s: str):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    lex = LexicalAnalyzer(s)
    sents = lex.process()

    comp_x = []
    for sent in sents:
        reph = ' '.join(sent)
        x_norm = normalize_str(reph)
        X = plots_3d(x_norm)
        comp_x.append(X)

    comp_x = comp_x[0]
    recomp_x = [list(x) for x in zip(*comp_x)]
    [print(x) for x in recomp_x]

    ax.scatter(recomp_x[0], recomp_x[1], recomp_x[2], marker='o')

    kmeans = KMeans(n_clusters=25)
    kmeans_labels = kmeans.fit_predict(comp_x)
    centroids = kmeans.cluster_centers_
    cluster_sizes = np.bincount(kmeans_labels)

    for i, (center, size) in enumerate(zip(centroids, cluster_sizes)):
        radius = size * 0.1
        plot_sphere(ax, center, radius, 'red')

    plt.show()


def main():
    myths_norse_path = Path("C:\\Users\\chris\\.databox\\texts\\myths_of_the_norsemen.txt")
    with open(myths_norse_path, 'rt', encoding='utf8') as f:
        txt = f.read()
    word_mechanism(str(txt))


if __name__ == "__main__":
    main()
