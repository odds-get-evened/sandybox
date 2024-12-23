from pathlib import Path

import pandas as pd


def main():
    green_power_path = Path("C:\\Users\\chris\\value-is-soul\\taber\\data\\water_supply_survey_datasets.xlsx")

    '''
    df = pd.ExcelFile(green_power_path)
    print(df.sheet_names)
    '''
    df = pd.read_excel(green_power_path, sheet_name='water_supply_curve')
    print(df)


if __name__ == "__main__":
    main()
