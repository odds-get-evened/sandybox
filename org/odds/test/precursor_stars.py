"""
A provisional list of stars compiled by the NASA Exoplanet Exploration
Program (ExEP)[https://exoplanets.nasa.gov/exep/science-overview/] that are most likely (given current knowledge) to constitute target
stars for the exo-Earth survey of the future Habitable Worlds Observatory (HWO)
mission.
"""
import os.path
from pathlib import Path

import pandas as pd

precursos_path = Path(os.path.expanduser('~'), '.databox', 'DI_STARS_EXEP_2024.12.11_15.40.33.csv')


def main():
    df = pd.read_csv(precursos_path, encoding='utf8', on_bad_lines='skip')
    print(df.columns)
    print(df[[
        'hip_name', 'hd_name', 'hr_name', 'gj_name', 'constellation',
        'hostname', 'sy_dist', 'ra', 'dec', 'st_rad', 'st_diam',
        'st_mass', ''
    ]])


if __name__ == "__main__":
    main()
