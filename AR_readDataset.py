#!/usr/bin/python
#
# Read the dataset, stem each review instances and 
# return test, train, and unlabeled data

# python imports
import os, glob, sys, re
# stemming
try:
	from nltk.stem.porter import PorterStemmer
except:
	print("Please install the module 'nltk' for stemming!")
	print("pip install nltk")
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

# read the dataset
# @param: the name of the dataset
# @return: train, test and unlabeled data after stemming and case-folding
#  each of them is a dict, e.g. train[1] = all the informative review instances
#                               train[-1] = all non-informative review instance
def AR_readDataset(datasetName):

	fileTrain = os.path.join( "./datasets", datasetName, "trainL")
	fileUnlabel = os.path.join("./datasets", datasetName, "trainU")
	fileTest = os.path.join("./datasets", datasetName, "test")

	cnt = 0

	# returns:
	train = {}
	test = {}
	unlabel = {}

	# for training set:
	info = os.path.join(fileTrain, "info.txt")
	cnt = readFile(info, train, cnt, 1)

	non_info = os.path.join(fileTrain, "non-info.txt")
	cnt = readFile(non_info, train, cnt, -1)

	# for testing set:
	info = os.path.join(fileTest, "info.txt")
	cnt = readFile(info, test, cnt, 1)

	non_info = os.path.join(fileTest, "non-info.txt")
	cnt = readFile(non_info, test, cnt, -1)


	# for unlabeled set:
	info = os.path.join(fileUnlabel, "unlabeled.txt")
	cnt = readFile(info, train, cnt, 0)

	return train, test, unlabel


# read the data file given the filename and return the dataset
# @dataset: train/test/unlabel, as dict, @cnt: for labeling;
# @label: 1 -> informative, -1 -> noninformative 0 -> unlabeled
def readFile(filename, dataset, cnt, label):
	if not os.path.isfile(filename):
		print('Given dataset not found: {}'.format(filename))
		return
	if(not dataset.has_key(label)):
		dataset[label] = []

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
			# stem the content:
			for t in tokens:
				t = stem_cached(t)
				content.append(t)

			ntokens = len(content)

			review = Review()
			review.fromText(cnt, content, ntokens, rating, label)
			# For debugging:
			review.printSelf()
			dataset[label].append(review)
			cnt += 1

	return cnt


