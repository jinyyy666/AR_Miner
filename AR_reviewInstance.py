#!/usr/bin/python
#
# Define the review instances
# 

import numpy as np

# Class that contains the information for each review:
class Review:
	# Constructor:
	def __init__(self):
		# the review id
		self.id = -1
		# the review content, as a list
		self.content = []
		# rating of this review (1-5):
		self.rating = -1
		# number of tokens in the review:
		self.ntokens = -1
		# the time stamp:
		self.ts = ""
		# each group belong to 
		self.group = ""
		# the probability
		self.prob = 0
		# the label for this review: 1-> informative; 0 -> unlabeled; -1 ->non-informative
		self.label = 0
		# doc vector:
		self.vdoc = None

	# intialize from reading each review instance from the dataset
	def fromText(self, id, content, ntokens, rating, label):
		self.id = id
		self.content = content
		self.ntokens = ntokens
		self.rating = rating
		self.label = label

	# change the review instance to a dictionary instance
	def toDist(self):
		reviewDict = {}
		reviewDict['id'] = self.id
		reviewDict['content'] = self.content
		reviewDict['rating'] = self.rating
		reviewDict['ntokens'] = self.ntokens
		reviewDict['ts'] = self.ts
		reviewDict['group'] = self.group
		reviewDict['prob'] = self.prob
		reviewDict['label'] = self.label
		reviewDict['vdoc'] = self.vdoc

		return reviewDict
	# Remove the terms (rare ones) of the content that are not in the dictionary
	def removeRareTerm(self, vocabulary):
		newcontent = []
		for term in self.content:
			if(vocabulary.has_key(term)):
				newcontent.append(term)

		self.content = newcontent
		self.ntokens = len(newcontent)

	# given an vocabulary, form as a doc vector
	def formDocVector(self, vocabulary):
		v = np.zeros(len(vocabulary), dtype = 'float')

		for term in self.content:
			v[vocabulary[term]] += 1
		self.vdoc = v
		return v

	def printSelf(self):
		tmp = " ".join(self.content)
		print("Review id: " + str(self.id) + " Rating: "+ str(self.rating) + " Content: " + tmp + " Ntokens: " + str(self.ntokens) + " TS: " + self.ts + " Group: " + self.group + " Prob: " + str(self.prob) + " label: " + str(self.label) )
		print(self.vdoc)
