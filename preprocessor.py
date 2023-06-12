import pandas as pd

athlete = pd.read_csv("D:\\III YEAR ASSIGNMENTS\\Kaggle Datasets\\Olympics\\athlete_events.csv")
region = pd.read_csv("D:\\III YEAR ASSIGNMENTS\\Kaggle Datasets\\Olympics\\noc_regions.csv")

def preprocess():
    global athlete, region
    # filter of summer olympics
    summer_olympics = athlete[athlete['Season'] == 'Summer']
    # merge with region
    summer_olympics = summer_olympics.merge(region, on='NOC', how='left')
    # dropping duplicates
    summer_olympics.drop_duplicates(inplace=True)
    # one hot encoding medals
    summer_olympics = pd.concat([summer_olympics, pd.get_dummies(summer_olympics['Medal'])], axis=1)
    return summer_olympics
