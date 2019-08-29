import torch 
import math


def softmax(tensor, base=math.exp(1)):
	""" 
	Converts a set of raw scores from a model into a 
	probability distribution via softmax.
		
	The probability distribution will be a set of real numbers
	such that each is in the 0-1 range and the sum is 1.0

	Assumes input is a pytorch tensor in the form: tensor([1.0, 4.0, 2.0, 3.0])
		
	Keyword arguments:
		tensor -- a pytorch tensor of any positive/negative real numbers.
		base -- the base for the exponential (default e)
	"""
	exps = base**tensor # exponential for each value in array
	
	sum_exps = torch.sum(exps) # sum of all exponentials
	prob_dist = exps / sum_exps # normalize exponentials 
	return prob_dist


def margin_confidence(prob_dist, sorted=False):
	""" 
	Returns the uncertainty score of a probability distribution using
	margin of confidence sampling in a 0-1 range where 1 is the most uncertain
	
	Assumes probability distribution is a pytorch tensor, like: 
		tensor([0.0321, 0.6439, 0.0871, 0.2369])
		
	Keyword arguments:
		prob_dist -- a pytorch tensor of real numbers between 0 and 1 that total to 1.0
		sorted -- if the probability distribution is pre-sorted from largest to smallest
	"""
	if not sorted:
		prob_dist, _ = torch.sort(prob_dist, descending=True)
		
	difference = (prob_dist.data[0] - prob_dist.data[1]) # sort probs so that largest is first
	margin_conf = 1 - difference 
	
	return margin_conf.item()
	

def ratio_confidence(prob_dist, sorted=False):
	""" 
	Returns the uncertainty score of a probability distribution using
	ratio of confidence sampling in a 0-1 range where 1 is the most uncertain
	
	Assumes probability distribution is a pytorch tensor, like: 
		tensor([0.0321, 0.6439, 0.0871, 0.2369])
				
	Keyword arguments:
		prob_dist --  pytorch tensor of real numbers between 0 and 1 that total to 1.0
		sorted -- if the probability distribution is pre-sorted from largest to smallest
	"""
	if not sorted:
		prob_dist, _ = torch.sort(prob_dist, descending=True) # sort probs so that largest is first		
		
	ratio_conf = prob_dist.data[1] / prob_dist.data[0]
	
	return ratio_conf.item()
	
	


def least_confidence(prob_dist, sorted=False):
	""" 
	Returns the uncertainty score of an array using
	least confidence sampling in a 0-1 range where 1 is the most uncertain
	
	Assumes probability distribution is a pytorch tensor, like: 
		tensor([0.0321, 0.6439, 0.0871, 0.2369])
				
	Keyword arguments:
		prob_dist -- a pytorch tensor of real numbers between 0 and 1 that total to 1.0
		sorted -- if the probability distribution is pre-sorted from largest to smallest
	"""
	if sorted:
		simple_least_conf = prob_dist.data[0] # most confident prediction
	else:
		simple_least_conf = torch.max(prob_dist) # most confident prediction
				
	num_labels = prob_dist.size(0) # number of labels
	
	normalized_least_conf = (1 - simple_least_conf) * (num_labels / (num_labels -1))
	
	return normalized_least_conf.item()



def entropy_score(prob_dist):
	""" 
	Returns the uncertainty score of a probability distribution using
	entropy score
	
	Assumes probability distribution is a pytorch tensor, like: 
		tensor([0.0321, 0.6439, 0.0871, 0.2369])
				
	Keyword arguments:
		prob_dist -- a pytorch tensor of real numbers between 0 and 1 that total to 1.0
		sorted -- if the probability distribution is pre-sorted from largest to smallest
	"""
	log_probs = prob_dist * torch.log2(prob_dist) # multiply each probability by its base 2 log
	raw_entropy = 0 - torch.sum(log_probs)

	normalized_entropy = raw_entropy / math.log2(prob_dist.size(0))
	
	return normalized_entropy.item()
	
	

