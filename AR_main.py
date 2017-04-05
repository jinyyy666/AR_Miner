#!/usr/bin/python
#
# Implementation of the AR Miner:
# "AR-Miner: Mining Informative Reviews for Developer from Mobile App MarketPlace"
#
# Authors:
# 1) Shanshan Li
# 2) Yingyezhe Jin
# 3) Tianshu Chu
# 4) Xiao Huang

# python imports
import os, numpy

# AR Miner imports
from AR_parse import AR_parse
from AR_reviewInstance import Review
from AR_emnb import AR_emnb

# The main method:
def main():

	# 0. Given the application, read the reviews and stem them
	datasetName = "facebook"
	# trainSet/testSet/unlabel: dictionary of {label, reviews} for review data
	# vocabulary: dictionary len = V and the positional index of each term in the doc vector
	rmStopWords = False # Removing stop words lead to information loss
	rmRareWords = True
	trainSet, testSet, unlabelSet, vocabulary = AR_parse(datasetName, rmStopWords, rmRareWords)

	# 1. Use the EM-NB to filter out the informative reviews
	# informMat: the informative reviews in X x V matrix from, X: documents size, V: vocabulary size
	# informRev: corresponding reviews wrapped as a list of review instances
	informMat, informRev = AR_emnb(trainSet, testSet, unlabelSet, vocabulary)

# call the main
if __name__ == "__main__":
	main()