#!/usr/bin/python
#
# Implementation of the AR Miner:
# "AR-Miner: Mining Informative Reviews for Developer from Mobile App MarketPlace"
#
# Authors:
# 1) Shanshan Li
# 2) Yingyezhe Jin
# 3) Tianshu Chu

# python imports
import os, numpy

# AR Miner imports
from AR_readDataset import AR_readDataset
from AR_reviewInstance import Review
# The main method:
def main():

	# 0. Given the application, read the reviews and stem them
	datasetName = "facebook"
	trainSet, testSet, unlabelSet = AR_readDataset(datasetName)



# call the main
if __name__ == "__main__":
	main()