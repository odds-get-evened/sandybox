import re
import secrets

import nltk
from nltk.corpus import stopwords
from hashies import big_end_int_64


# import numpy as np

phrases = {
    'long_sentences': [
        "As the sun began to set over the horizon, painting the sky in shades of orange and pink, a gentle breeze rustled the leaves of the ancient oak tree that stood alone in the vast, open field, where generations of families had come to picnic and enjoy the serene beauty of nature.",
        "The old, weathered lighthouse, standing tall and proud on the edge of the rocky coastline, had guided countless ships safely to shore with its unwavering beam of light, even during the fiercest of storms when the waves crashed violently against the cliffs below.",
        "In a small, bustling village nestled in the heart of the mountains, the annual harvest festival brought together people from near and far, celebrating with music, dancing, and feasting on the bountiful produce that the fertile soil had generously provided that year.",
        "With the first light of dawn breaking through the dense canopy of the rainforest, the calls of exotic birds echoed through the trees, awakening the vibrant ecosystem teeming with life, from the smallest insects to the majestic jaguars stealthily prowling the forest floor.",
        "As the train chugged along the winding tracks, weaving through picturesque countryside and charming towns, passengers gazed out the windows at the ever-changing scenery, each lost in their own thoughts and stories, as the journey brought them closer to their destinations.",
        "In the grand, opulent ballroom of the ancient castle, chandeliers glittered with hundreds of candles, illuminating the elegant guests who danced gracefully to the melodies of a live orchestra, their laughter and conversation filling the air with a sense of timeless enchantment.",
        "The scientist, surrounded by a labyrinth of books and papers in her cluttered office, diligently worked late into the night, driven by a relentless curiosity and the hope of making a groundbreaking discovery that could change the world and benefit future generations.",
        "High above the bustling city streets, in a sleek, modern skyscraper, the executive looked out over the sprawling metropolis, contemplating the challenges and opportunities that lay ahead, as the city's lights twinkled like stars in the deepening twilight.",
        "On the arid plains of the savannah, a herd of elephants marched steadily towards a distant watering hole, their massive silhouettes silhouetted against the setting sun, while nearby, a pride of lions lounged in the shade, eyeing the potential prey with lazy interest.",
        "Amidst the chaotic hustle and bustle of the crowded marketplace, vendors shouted their wares, colorful stalls overflowed with exotic goods, and the air was thick with the aromas of spices and street food, creating a vibrant tapestry of sights, sounds, and smells that captivated all who wandered through."
    ]
}

def normalize_arr(arr, t_min, t_max):
    norm_arr = []

    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)

    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min

        norm_arr.append(temp)

    return norm_arr


def normalize_str(s: str) -> list[int]:
    # all to lowercase
    s = s.lower()
    # remove numbers
    s = re.sub(r'\d+', '', s)
    # remove everything except words and spaces
    s = re.sub(r'[^\w\s]', '', s)

    try:
        stopw = set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords', quiet=True)
        stopw = set(stopwords.words('english'))

    # remove stopwords and convert all strings to integer hash
    s_ls = [big_end_int_64(w.encode('utf8')) for w in s.split(' ') if w not in stopw]
    # normalize
    s_ls = normalize_arr(s_ls, -1, 1)

    return s_ls


def plots_2d(arr):
    new_arr = []

    for i in range(len(arr)):
        plot = None

        if i * 2 < len(arr):
            plot = [arr[i * 2]]

        if i * 2 + 1 < len(arr):
            plot.append(arr[i * 2 + 1])

        if plot is not None:
            new_arr.append(plot)

    return new_arr


def plots_3d(arr):
    new_arr = []

    # pad list to be divisible by 3
    mod = len(arr) % 3
    if mod > 0:
        pad_size = 3 - mod
        arr += [0] * pad_size

    for i in range(len(arr)):
        plot = None

        if i * 3 < len(arr):
            plot = [arr[i * 3]]

        if i * 3 + 1 < len(arr):
            plot.append(arr[i * 3 + 1])

        if i * 3 + 2 < len(arr):
            plot.append(arr[i * 3 + 2])

        if plot is not None:
            new_arr.append(plot)

    return new_arr


def main():
    # s = "You don’t have to be into the wilderness to enjoy camping. Tom doesn't want to make a big deal out of it. Our competitors don't normally ask us for advice, but when an airline leader reached out, we couldn't ignore it."
    s = secrets.choice(phrases['long_sentences'])
    plot = plots_3d(normalize_str(s))
    print(plot)
    # print(plots_3d(normalize_str(s)))


if __name__ == "__main__":
    main()
