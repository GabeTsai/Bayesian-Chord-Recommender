import numpy as np 
import pandas as pd
import json

def createDataset(filePath):
    """
    :param filePath: String, the path to the file containing the chord progressions.
    :return: List of dictionaries, the data for the Bayesian Network, following this format below:
    data = [
    {"Current Chord": "I", "Next Chord": "IV", "Key Type": "Major", "Musical Style": "Pop"},
    {"Current Chord": "IV", "Next Chord": "V", "Key Type": "Major", "Musical Style": "Pop"},
    {"Current Chord": "V", "Next Chord": "I", "Key Type": "Major", "Musical Style": "Pop"},
    # Additional entries for other progressions and styles
    ]
    """
    chordData = pd.read_csv(filePath).to_numpy()
    print(chordData)
    data = []
    for i in range(len(chordData)):
        chordsList = chordData[i][1].split()
        chordKey = chordData[i][0].lower()
        chordMusicalStyles = chordData[i][2].lower().replace(',', '').split()
        for j in range(len(chordsList) - 1):
            data.append({"Current Chord": chordsList[j], "Next Chord": chordsList[(j+1)], "Key Type": chordKey, "Musical Style": chordMusicalStyles[0]})
            if len(chordMusicalStyles) > 1:
                data.append({"Current Chord": chordsList[j], "Next Chord": chordsList[(j+1)], "Key Type": chordKey, "Musical Style": chordMusicalStyles[1]})

    return data

def loadData(filePath):
    """
    Load the data from the JSON file and convert it to a DataFrame.
    :param filePath: String, the path to the JSON file containing the data.
    :return: DataFrame, the data for the Bayesian Network.
    """
    data = pd.read_json(filePath)
    return pd.DataFrame(data)

def main():
    filePath = 'chords.csv'
    with open('chordData.json', 'w') as f:
        json.dump(createDataset(filePath), f)

if __name__ == "__main__":
    main()