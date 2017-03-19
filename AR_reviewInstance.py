#!/usr/bin/python
#
# Define the review instances
# 

from collections import namedtuple

# Class that contains the information for each review:
class Review:
	# Constructor:
	def __init__(self):
		# the review id
		self.id = -1
		# the review content, as a list
		self.content = []
		# number of tokens this review contains
		self.ntokens = 0
		# rating of this review (1-5):
		self.rating = -1
		# the time stamp:
		self.ts = ""
		# each group belong to 
		self.group = ""
		# the probability
		self.prob = 0
		# the label for this review: 1-> informative; 0 -> unlabeled; -1 ->non-informative
		self.label = 0

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
		reviewDict['ntokens'] = self.ntokens
		reviewDict['rating'] = self.rating
		reviewDict['ts'] = self.ts
		reviewDict['group'] = self.group
		reviewDict['prob'] = self.prob
		reviewDict['label'] = self.label
		return reviewDict

	def printSelf(self):
		tmp = " ".join(self.content)
		print("Review id: " + str(self.id) + " Rating: "+ str(self.rating) + " Content: " + tmp + " Ntokens: " + str(self.ntokens) + " TS: " + self.ts + " Group: " + self.group + " Prob: " + str(self.prob) + " label: " + str(self.label) )
