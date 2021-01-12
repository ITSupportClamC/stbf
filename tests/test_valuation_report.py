# coding=utf-8
# 

import unittest2
from stbf.valuation_report import getCurrentDirectory \
									, getValuationDataFromFile
from os.path import join



class TestValuationReportSteven(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestValuationReportSteven, self).__init__(*args, **kwargs)


	def testGetValuationDataFromFile(self):
		file = join(getCurrentDirectory(), 'samples', 'InvestValSTBF_testcase1.xls')
		date, currency, fixedDeposit, bondPositions, cashPositions = \
			getValuationDataFromFile(file)

		self.assertEqual('2021-01-06', date)
		self.assertEqual('USD', currency)

		fixedDeposit = list(fixedDeposit)
		self.assertEqual(9, len(fixedDeposit))
		self.verifyFixedDeposit(fixedDeposit[0])

		bondPositions = list(bondPositions)
		self.assertEqual(7, len(bondPositions))
		self.verifyBondPosition(bondPositions[0])

		cashPositions = list(cashPositions)
		self.assertEqual(2, len(cashPositions))
		self.verifyCashPosition(cashPositions[1])



	def verifyFixedDeposit(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'CHINA MINSHENG BANKING CORP LTD, HK BRANCH TIME DEPOSIT-USD'
						, p['INVESTMENT'])
		self.assertEqual('', p['ISIN CODE'])
		self.assertEqual('', p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual('', p['AVG UNIT PRICE'])
		self.assertEqual(9700660.14, p['ORIG CURR BOOK COST'])
		self.assertEqual(9700660.14, p['PORT CURR BOOK COST'])
		self.assertEqual('', p['MARKET PRICE'])
		self.assertEqual(9700660.14, p['ORIG CURR MKT VALUE'])
		self.assertEqual(9700660.14, p['PORT CURR MKT VALUE'])
		self.assertEqual(177.85, p['ACCR INT PORT CCY'])
		self.assertEqual(19.81, p['% OF TOTAL'])
		self.assertEqual(0, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2021-01-05', p['VALUE DATE'])
		self.assertEqual(0.33, p['INT RATE'])
		self.assertEqual('2021-01-12', p['MATURITY DATE'])



	def verifyBondPosition(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'randomise'
						, p['INVESTMENT'])
		self.assertEqual('XS1496345684', p['ISIN CODE'])
		self.assertEqual(4800000.0000, p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual(100.980000, p['AVG UNIT PRICE'])
		self.assertEqual(4847040, p['ORIG CURR BOOK COST'])
		self.assertEqual(4847040, p['PORT CURR BOOK COST'])
		self.assertEqual(101.027, p['MARKET PRICE'])
		self.assertEqual(4849296, p['ORIG CURR MKT VALUE'])
		self.assertEqual(4849296, p['PORT CURR MKT VALUE'])
		self.assertEqual(45266.67, p['ACCR INT PORT CCY'])
		self.assertEqual(9.90, p['% OF TOTAL'])
		self.assertEqual(2256.00, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2016-09-26', p['VALUE DATE'])
		self.assertEqual(3.5, p['INT RATE'])
		self.assertEqual('2021-09-30', p['MATURITY DATE'])



	def verifyCashPosition(self, p):
		self.assertEqual(14, len(p))
		self.assertEqual( 'USD CASH AC - BANK OF CHINA (UK)'
						, p['INVESTMENT'])
		self.assertEqual('', p['ISIN CODE'])
		self.assertEqual('', p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual('', p['AVG UNIT PRICE'])
		self.assertEqual(11893800.03, p['ORIG CURR BOOK COST'])
		self.assertEqual(11893800.03, p['PORT CURR BOOK COST'])
		self.assertEqual('', p['MARKET PRICE'])
		self.assertEqual(11893800.03, p['ORIG CURR MKT VALUE'])
		self.assertEqual(11893800.03, p['PORT CURR MKT VALUE'])
		self.assertEqual('', p['ACCR INT PORT CCY'])
		self.assertEqual(25.67, p['% OF TOTAL'])
		self.assertEqual(0, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])