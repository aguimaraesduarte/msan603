from numpy import random
import numpy as np
import sys

# second price
def sp(n):
	BidF = []
	for rnd in random.uniform(0,1, size = [1,n])[0]:
		f = lambda currentBid, bidHist, rnd2=rnd: rnd2
		BidF.append( f )
	return BidF


# first price
def fp(n):
	BidF = []
	for rnd in random.uniform(0, 1, size = [1,n])[0]:
		f = lambda currentBid, bidHist, rnd2=rnd: (n-1) * rnd2 / float(n)
		BidF.append( f )
	return BidF


def bh2(currentBid, bidHistory, rnd2):
	if len( bidHistory ) > 1:
		## Handle the first round which would have no bidHistory
		if currentBid < rnd2:
			return 1
		else:
			return 0
		"""
		if 1.0*sum(bidHistory[-1][’Bids’]) / len(bidHistory[-1][’Bids’]) < .5 and currentBid < 5:
			return 1
		else:
			return 0
		"""
	else:
		### If there is no bid history then don’t bid.
		return 0


def oo(n):
	BidF = []
	for rnd in random.uniform(0, 1, size = [1,n])[0]:
		f = lambda currentBid, bidHistory, rnd2=rnd: 1 if currentBid<rnd2 else 0
		BidF.append( f )
	return BidF


def incrementBidHistory(bidHistory, bidderInfo, value):
	rnd = len(bidHistory)+1
	bids = []
	for row in bidderInfo:
		bids.append(row["BidFunction"](value, bidHistory))
	bh = bidHistory
	bh.append({"Round": rnd,
		       "Value": value,
		       "Bids": bids})
	#print rnd, bids, bh
	return bh


def auctionEvaluator(priceFormat, auctionFormat, bidHistory, bidderInfo, value=None, increment=None):
	if auctionFormat == "SB":
		bids = []
		bidders = []
		for row in bidderInfo:
			bids.append(row["BidFunction"](None, bidHistory))
			bidders.append(row["BidderName"])
		zipped = sorted(zip(bids, bidders))
		bids, bidders = zip(*zipped)
		#print bids
		#print bidders
		return (bids[-priceFormat], bidders[-1])
	elif auctionFormat == "OO":
		bh = incrementBidHistory(bidHistory, bidderInfo, value)
		if np.sum(bh[-1]["Bids"]) == 1:
			#print "winner found"
			winner_index = bh[-1]["Bids"].index(1)
			winnerName = bidderInfo[winner_index]["BidderName"]
			winnerBid = value - (priceFormat - 1)*increment
			return (winnerName, winnerBid)
		elif np.sum(bh[-1]["Bids"]) == 0:
			try:
				winner_indices = [i for i, j in enumerate(bh[-2]["Bids"]) if j == 1]
				winner_index = random.choice(winner_indices)
			except:
				return ("No winner", -1)
			winnerName = bidderInfo[winner_index]["BidderName"]
			winnerBid = value - (priceFormat - 1)*increment
			return (winnerName, winnerBid)
		else:
			#print "no winner yet"
			v = value + increment
			return auctionEvaluator(priceFormat, auctionFormat, bh, bidderInfo, v, increment)
	else:
		return ("Not a valid auction format. Should be 'SB' or 'OO'.")

# testing
### a) 
##### SB, second price, 10 bidders, valuations 0, .1, .2, ..., .9
bidFunctions = sp(10)
bidderNames = ["Bidder"+str(x) for x in range(1,11)]
BI = []
for i in range(10):
	BI.append({"BidderName": bidderNames[i],
		       "BidFunction": bidFunctions[i]})
auctionEvaluator(2, "SB", [], BI)


### b)
##### SB, first price, 10 bidders, valuations 0, .1, .2, ..., .9
bidFunctions = fp(10)
bidderNames = ["Bidder"+str(x) for x in range(1,11)]
BI = []
for i in range(10):
	BI.append({"BidderName": bidderNames[i],
		       "BidFunction": bidFunctions[i]})
auctionEvaluator(1, "SB", [], BI)


### c)
##### OO, second price, 10 bidders, valuations 0, .1, .2, ..., .9, value=0, increment=0.05
bidFunctions = oo(10)
bidderNames = ["Bidder"+str(x) for x in range(1,11)]
BI = []
for i in range(10):
	BI.append({"BidderName": bidderNames[i],
		       "BidFunction": bidFunctions[i]})
auctionEvaluator(2, "OO", [], BI, 0, 0.05)