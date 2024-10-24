import os.path
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
from verble.lexicon import LexicalAnalyzer, normalize_arr, normalize_str, plots_2d

PHRASES = [
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


def main():
    # plt.figure(figsize=(10, 6))
    for phrase in PHRASES:
        lex = LexicalAnalyzer(phrase)
        sents = lex.process()
        reph = ' '.join(sents[0])
        # 1 dimension
        x_nums = normalize_str(reph)
        X = split_list_fit(x_nums)
        # print(X)
        # print()
        trans_x = list(map(list, zip(*X)))

        tree = KDTree(trans_x)
        print(f"kernel density {tree.kernel_density(trans_x[:3], h=0.1, kernel='gaussian')}")

        # [print(x) for x in trans_x]
        # plt.scatter(x=trans_x[0], y=trans_x[1])
    # plt.show()


if __name__ == "__main__":
    main()
