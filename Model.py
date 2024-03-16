from pgmpy.models import BayesianNetwork
from pgmpy.estimators import ParameterEstimator, MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination
import pandas as pd
import numpy as np
import networkx as nx  
import matplotlib.pyplot as plt
from CreateDataset import loadData
import pickle
import random

class BayesianModel:
    def __init__(self):
        self.model = BayesianNetwork([
            ("Current Chord", "Next Chord"),  # Current chord influences the next chord.
            ("Key Type", "Current Chord"),  # Key type influences the current chord.
            ("Key Type", "Next Chord"),  # Key type influences the next chord.
            ("Musical Style", "Current Chord"),  # Musical style influences the current chord
            ("Musical Style", "Next Chord")  # Musical style influences the next chord.
        ])

    def visualizeModel(self):
        modelGraph = nx.DiGraph()
        modelGraph.add_edges_from(self.model.edges())  # generate edges
        pos = nx.spring_layout(modelGraph)  # Generate a layout for the nodes
        nx.draw(modelGraph, pos, with_labels=True, node_size=8000, node_color="lightblue", font_size=10,
                font_weight="bold")

        plt.title("Bayesian Network Model")
        plt.axis('off')
        plt.show()

    def train(self, data):
        """
        Calculate the CPDs using the Maximum Likelihood Estimator (given the current chord, key type and musical style, how likely is chord X as the next chord?).

        :param data: DataFrame, the data for the Bayesian Network.
        """
        self.model.fit(data, estimator=BayesianEstimator, prior_type='dirichlet', pseudo_counts=1)  # Use the Bayesian Estimator with Laplace smoothing to train the model
        with open('bayesianChordNetwork.pkl', 'wb') as f:
            pickle.dump(self.model, f)
    
    def inferNextChords(self, currentChord, keyType, musicalStyle):
        """
        Infer the next chord given the current chord, key type, and musical style.
        :param currentChord: String, the current chord.
        :param keyType: String, the key type.
        :param musicalStyle: String, the musical style.
        :return: String, the next chord.
        """
        inference = VariableElimination(self.model)
        return inference.query(variables = ['Next Chord'], evidence = {'Current Chord': currentChord, 'Key Type': keyType, 'Musical Style': musicalStyle})

    def loadModel(self, filePath):
        """
        Load the trained model from a file.
        :param filePath: String, the path to the file containing the trained model.
        """
        with open(filePath, 'rb') as f:
            self.model = pickle.load(f)

    def recommendChords(self, currentChord, keyType, musicalStyle):
        """
        Recommends top three chords (chords with largest ) given the current chord, key type, and musical style.
        Chooses chord from top three largest conditional probabilities.
        :param currentChord: String, the current chord.
        :param keyType: String, the key type.
        :param musicalStyle: String, the musical style, pop or classical. 
        :return: String, the recommended next chord.
        """
        # Perform inference to get the probability distribution of 'Next Chord'
        inferredChords = self.inferNextChords(currentChord, keyType, musicalStyle)

        # Extract the probability values and state names (chords)
        probabilities = inferredChords.values
        chord_names = inferredChords.state_names['Next Chord']

        # Randomly choose from top 3 probabilities (largest to smallest)
        chosen_indices = np.argsort(-probabilities)[:3]

        recommended_chords = []
        for index in chosen_indices:
            recommended_chords.append(chord_names[index])

        return recommended_chords

def main():
    #Example Usage
    data = loadData('chordData.json')
    bayesianNetwork = BayesianModel()
    bayesianNetwork.train(data)
    bayesianNetwork.visualizeModel()
    recommendedChords = bayesianNetwork.recommendChords('V', 'major', 'classical')
    print(recommendedChords)

if __name__ == "__main__":
    main()