from collections import defaultdict
import operator

prop_threshold = 0.01
sim_threshold = 0.6
topics_num = 20
# topic_revs = defaultdict(list)
# topic_revs_prop = defaultdict(dict)
# topic_revs_rating = defaultdict(dict) 
# topic_revs_duplic = defaultdict(dict)
# topic_revs_probab = defaultdict(dict)
# updated_topic_revs_prop = defaultdict(dict)
# updated_topic_revs_rating = defaultdict(dict) 
# updated_topic_revs_probab = defaultdict(dict)

def group_revs(doc_topic):
	topic_revs = defaultdict(list)

	for i in range(len(doc_topic)):
		for j in range(topics_num):
			if doc_topic[i][j] >= prop_threshold:
				topic_revs[j].append(i)

	# for j in range(len(topic_revs)):
	# 	print len(topic_revs[j])
	return topic_revs

def rev_prop(doc_topic):
	topic_revs_prop = defaultdict(dict)
	topic_revs = group_revs(doc_topic)

	for topic in topic_revs:
		for rev_idx in topic_revs[topic]:
			topic_revs_prop[topic][rev_idx] = doc_topic[rev_idx][topic]
	return topic_revs_prop

def rev_rating(doc_topic, informRev):
	topic_revs_rating = defaultdict(dict) 
	topic_revs = group_revs(doc_topic)
	
	for topic in topic_revs:
		for rev_idx in topic_revs[topic]:
			topic_revs_rating[topic][rev_idx] = 1/float(informRev[rev_idx].rating)
	return topic_revs_rating

def rev_probab(doc_topic, informRev):
	"""
	calculating review instance posterior probability through EMNB
	"""
	topic_revs_probab = defaultdict(dict)
	topic_revs = group_revs(doc_topic)
	
	for topic in topic_revs:
		for rev_idx in topic_revs[topic]:
			topic_revs_probab[topic][rev_idx] = informRev[rev_idx].prob
	return topic_revs_probab


def JaccardSimilarity(x, y):    
	intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
	union_cardinality = len(set.union(*[set(x), set(y)]))
	if union_cardinality==0:
		return 0.0
	else:
		jaccard=intersection_cardinality/union_cardinality
		return jaccard
	
def rev_duplic(doc_topic, informRev): 
	topic_revs_duplic = defaultdict(dict)
	updated_topic_revs_prop = defaultdict(dict)
	updated_topic_revs_rating = defaultdict(dict)
	updated_topic_revs_probab = defaultdict(dict)
	topic_revs = group_revs(doc_topic)
	topic_revs_prop = rev_prop(doc_topic)
	topic_revs_rating = rev_rating(doc_topic, informRev)
	topic_revs_probab = rev_probab(doc_topic, informRev)
	
	for topic in topic_revs:  
		rev_simRevs = defaultdict(list)
		for i in range(len(topic_revs[topic])):
			rev_idx1 = topic_revs[topic][i]
			if rev_simRevs:
				for key in rev_simRevs.keys():
					if rev_idx1 in rev_simRevs[key]:
						continue      
			VS1 = informRev[rev_idx1].content
			rev_simRevs[rev_idx1] = []
			for j in range(i+1,len(topic_revs[topic])):                
				rev_idx2 = topic_revs[topic][j]                
				VS2 = informRev[rev_idx2].content
				textSim = JaccardSimilarity(VS1, VS2)
				if textSim >= sim_threshold:
					rev_simRevs[rev_idx1].append(rev_idx2)
		for rev_key in rev_simRevs.keys():
			topic_revs_duplic[topic][rev_key] = len(rev_simRevs[rev_key])
			if not rev_simRevs[rev_key]:
				updated_topic_revs_prop[topic][rev_key] = topic_revs_prop[topic][rev_key]
				updated_topic_revs_rating[topic][rev_key] = topic_revs_rating[topic][rev_key]
				updated_topic_revs_probab[topic][rev_key] = topic_revs_probab[topic][rev_key]
			rev_simRevs[rev_key].append(rev_key)
			dupli_prop_dict = dict((rev_dupli, topic_revs_prop[topic][rev_dupli]) for rev_dupli in rev_simRevs[rev_key])
			dupli_rating_dict = dict((rev_dupli, 1/float(informRev[rev_dupli].rating)) for rev_dupli in rev_simRevs[rev_key])
			dupli_probab_dict = dict((rev_dupli, topic_revs_probab[topic][rev_dupli]) for rev_dupli in rev_simRevs[rev_key])
			maxKeyProp = max(dupli_prop_dict.iteritems(), key=operator.itemgetter(1))[0]
			maxKeyRating = max(dupli_rating_dict.iteritems(), key=operator.itemgetter(1))[0]
			maxKeyProbab = max(dupli_probab_dict.iteritems(), key=operator.itemgetter(1))[0]
			updated_topic_revs_prop[topic][rev_key] = dupli_prop_dict[maxKeyProp]
			updated_topic_revs_rating[topic][rev_key] = dupli_rating_dict[maxKeyRating]
			updated_topic_revs_probab[topic][rev_key] = dupli_probab_dict[maxKeyProbab]

	return topic_revs_duplic, updated_topic_revs_prop, updated_topic_revs_rating, updated_topic_revs_probab
	
def instance_ranking(doc_topic, weight, informRev):
	topic_revs_duplic, updated_topic_revs_prop, updated_topic_revs_rating, updated_topic_revs_probab = rev_duplic(doc_topic, informRev)
	topic_revs_top10Rank = defaultdict(dict)    
	for topic in topic_revs_duplic:
		rev_importanceScore_dict = {}
		for key in topic_revs_duplic[topic].keys():
			rev_importanceScore_dict[key] = weight[0] * updated_topic_revs_prop[topic][key] + \
											weight[1] * topic_revs_duplic[topic][key] + \
											weight[2] * updated_topic_revs_rating[topic][key] + \
											weight[3] * updated_topic_revs_probab[topic][key]
		top10_rev_importanceScore = sorted(rev_importanceScore_dict.items(), key=operator.itemgetter(1))[::-1][:10]
		topic_revs_top10Rank[topic] = top10_rev_importanceScore
	return topic_revs_top10Rank
		