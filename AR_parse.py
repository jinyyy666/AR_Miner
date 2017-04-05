#!/usr/bin/python
#
# Read the dataset, stem each review instances and 
# return test, train, and unlabeled data
# Author: Yingyezhe Jin; Date: Mar. 19, 2017

# python imports
import os, glob, sys, re
import numpy as np

# stemming and removing stop words
try:
	from nltk.stem.porter import PorterStemmer
except:
	print("Please install the module 'nltk' for stemming and removing stop words!")
	print("pip install nltk")
	sys.exit(-1)
try:
	from nltk.corpus import stopwords
except:
	print("Please install the nltk.corpus...")
	print("Please do the following in python:")
	print(">>> import nltk")
	print(">>> nltk.download('all')")
	sys.exit(-1)

# AR imports
from AR_reviewInstance import Review

# convert the rating to actual number
rating2int = {"zero" : 0, "one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5}

# the caching idea for speeding up the parser:
cache={}
st = PorterStemmer()

def stem_cached(token):
    if token not in cache:
        cache[token] = st.stem(token)
    return cache[token]

# stop words
operators = set(('and', 'or', 'not', 'is', 'are'))
stopWords = set(stopwords.words("english")) - operators

# read the dataset
# @param: the name of the dataset
# @return: train, test and unlabeled data after stemming and case-folding
def AR_parse(datasetName, rmStopWords, rmRareWords):

	fileTrain = os.path.join( "./datasets", datasetName, "trainL")
	fileUnlabel = os.path.join("./datasets", datasetName, "trainU")
	fileTest = os.path.join("./datasets", datasetName, "test")

	cnt = 0

	# returns:
	train = []
	test = []
	unlabel = []

	vocabulary = {}

	# 1. Read the dataset and form a vocabulary
	# for training set:
	info = os.path.join(fileTrain, "info.txt")
	cnt = readFile(info, train, 1, vocabulary, cnt, rmStopWords)

	non_info = os.path.join(fileTrain, "non-info.txt")
	cnt = readFile(non_info, train, -1, vocabulary, cnt, rmStopWords)

	# for testing set:
	info = os.path.join(fileTest, "info.txt")
	cnt = readFile(info, test, 1, vocabulary, cnt, rmStopWords)

	non_info = os.path.join(fileTest, "non-info.txt")
	cnt = readFile(non_info, test, -1, vocabulary, cnt, rmStopWords)


	# for unlabeled set:
	info = os.path.join(fileUnlabel, "unlabeled.txt")
	cnt = readFile(info, train, 0, vocabulary, cnt, rmStopWords)

	# 2. Remove the rare words (occur only once)
	if(rmRareWords == True):
		newVoc = {}
		for term, index in vocabulary.items():
			if(index > 1):
				newVoc[term] = len(newVoc)
	else:
		newVoc = vocabulary

	assert(bool(newVoc))
	print("New vocabulary size: " + str(len(newVoc)))

	if(rmRareWords == True):
		for review in train:
			review.removeRareTerm(newVoc)
			review.printSelf()
		for review in test:
			review.removeRareTerm(newVoc)
			review.printSelf()
		for review in unlabel:
			review.removeRareTerm(newVoc)
			review.printSelf()


	return train, test, unlabel, newVoc


# read the data file given the filename and return the dataset
# @dataset: train/test/unlabel, as dict, @cnt: for labeling;
# @label: 1 -> informative, -1 -> noninformative 0 -> unlabeled
# @voc: vocabulary a dict {term, positional index}
def readFile(filename, dataset, label, voc, cnt, rmStopWords):
	if not os.path.isfile(filename):
		print('Given dataset not found: {}'.format(filename))
		return


	with open(filename, 'r') as f:
		# read each review instance line by line:
		for instance in f:
			# break each line into three parts, ignore the first segment:
			parts = instance.split(' ')		
			r = parts[1] # like: ratingone
			rating = rating2int[r[6:]]
			text = " ".join(parts[2:]) # like: blabla blabla...
			
			# case-folding

			text = text.lower()
			# remove the non-alpha-number words
			tokens = re.findall(r'\w+', text)
			content = []
			# stem the content and remove stop words:
			for t in tokens:
				if(rmStopWords == True and t in stopWords):
					continue

				t = stem_cached(t)
				content.append(t)
				# build the vocabulary
				if(not voc.has_key(t)):
					voc[t] = len(voc)

			ntokens = len(content)

			review = Review()
			review.fromText(cnt, content, ntokens, rating, label)
			# For debugging:
			review.printSelf()
			dataset.append(review)
			cnt += 1

	return cnt


