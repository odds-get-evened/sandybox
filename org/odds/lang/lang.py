import os.path
from pathlib import Path

import nltk
import numpy as np

from org.odds.lang.lexical import normalize_str, plots_3d, LexicalAnalyzer

# update mine with a local path
nltk.data.path.append('C:\\Users\\chris\\AppData\\Local\\databox\\nltk')

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


def process_lexicon(a: list[list[str]]):
    p = []

    for sent in a:
        normed = normalize_str(' '.join(sent), t_min=-1, t_max=1)
        qub = plots_3d(normed)
        p.append(qub)

    return p


def do_lexical_analysis(s: str):
    s = s.strip().lower()

    proc = LexicalAnalyzer(s, max_workers=8).process()
    plots = process_lexicon(proc)
    [print(len(plot)) for plot in plots]
    plots_1d = np.array(plots).flatten().tolist()


def main():
    with open(Path(os.path.expanduser('~'), ".databox", "texts", "nature-rwemerson.txt"), 'rt', encoding='utf-8') as f:
        words_and_stuff = f.read()

    do_lexical_analysis(words_and_stuff)


if __name__ == "__main__":
    main()
