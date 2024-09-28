## Bayesian Chord Recommender

Chord progressions are successions of chords that form the foundational harmony of musical pieces from the Baroque period that marked the start of the Classical music era to works from the 21st century. 
Countless musical pieces reuse the same common chord progressions, because these progressions often have the universal ability to lay the grounds for complex and beautiful music. 
Therefore, we can use principles of conditional probability and build a Bayesian network to predict what chord could follow a chord, given information about the mode (major or minor) of the piece, musical style, and more.

### Data Collection

I scoured the internet and poured in my personal experience with music (I have been playing the piano for around 14 years, violin for over 12 years) and recorded 34 common chord progressions. For each chord progression, I included the mode (major or minor), and the genre that the progression was most commonly used in. Since the Bayesian network is quite simple, I included only two genres - classical and pop. In addition, all of the chords are triads. The chord progressions used to train the Bayesian network are listed below. A lowercase b in front of a chord means that its root note is lowered by a half step, and a d in front of a chord means that the chord is diminished. The data I collected is linked [here](https://docs.google.com/spreadsheets/d/1Co6UHF5Mic6cjz6ZQ29I1xgM_ckQGoKB5IN9Hx3GLIc/edit?usp=sharing). 

 
In order to encode this data into the Bayesian network, I wrote a chord class to be able to generate triad chord names given the minor or major key of the music. I consulted GPT 4 for a way to encode my data into a Bayesian network that could recommend another chord based on that given information, and settled on the following solution: I created a dataset as a list of dictionaries, where each dictionary contained the roman numeral of the current chord, the roman numeral of the next chord, the key type (major or minor), and the musical style (classical or pop). This data format is highly compatible with a python Bayesian network library I used called pgmpy. 

### The Model Architecture

The Bayesian Chord Progression Generator is a simple Bayesian network parameterized according to the diagram below, where the arrows represent node dependencies. I decided on these relationships based on my own music knowledge. For example, it is reasonable to assume that the key type can affect the next chord and the current chord (certain chords are more commonly used in minor than major keys). As with all Bayesian Networks, the nodes are conditionally independent of their non-descendants given their parents. I decided on a first-order Markov model for the Bayesian network to set a reasonable scope for the project, meaning that a chord would depend on the preceding chord. 

### Training the Model

I trained the Bayesian network using the Dirichlet prior distribution (the multinomial version of the Beta distribution) for each node, since I’m trying to calculate the conditional probability of a chord showing up based on several multinomial or categorical variables - the chord that preceded it, musical genre, and key type. In addition, the Dirichlet distribution is the conjugate prior of the multinomial distribution, similar to how the Beta distribution is the conjugate prior of the Bernoulli and thus binomial distribution, so calculating the posterior distribution is as easy as updating the distribution’s parameters with the number of occurrences of each event.


We’re working with sparse data here - there are 17 different types of chords in our dataset, and only 34 chord progressions. This means that a lot of chord pairings will not show up, which will lead to probabilities with values zero. Thus, I also employed Laplace smoothing in combination with the Dirichlet prior distributions to ensure that every conditional event occurred at least once to prevent zero probabilities, creating a more useful network. 

### Chord Recommendations

The network performs an inference on the probability of the next chord’s roman numeral value given the roman numeral of the current chord, the key, and the music genre type. 
In a normal Bayesian network, we would recommend the highest conditional probabilities, but to spice things up, I had the network recommend the top three highest conditional probabilities so that way the user could pick from those three chords to customize their chord progression.
	
### User Interface

I coded a rough user interface with Tkinter to allow a user to play around with the network. The user needs to select the key type, key, music type and the roman numeral of the starting chord. They can then continuously generate a chord progression based on the Bayesian network’s top three recommendations, and quit any time when they’ve had their fun.
