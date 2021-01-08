# coding=utf-8
#
# Functions to read valuation report from BOCI-Prudential valuation
# report.
# 
from os.path import abspath, dirname



def getValuationDataFromFile(file):
	"""
	[String] file (daily valuation report for Short Term Bond Fund)
		=> [Tuple] ( [String] date (yyyy-mm-dd)
				   , [String] portfolio currency
				   , [Iterable] fixed deposit positions
				   , [Iterable] bond positions
				   , [Iterable] bank balance positions
				   )
	"""
	# FIXME: to be implemented
	return ('', '', [], [], [])



"""
	returns the current directory

	for running the test case provided
"""
getCurrentDirectory = lambda : \
	dirname(abspath(__file__))



