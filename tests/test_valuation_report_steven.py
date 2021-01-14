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
		file = join(getCurrentDirectory(), 'samples', 'sample InvestValSTBF.xls')
		date, currency, fixedDeposit, bondPositions, cashPositions = \
			getValuationDataFromFile(file)

		self.assertEqual('2021-01-06', date)
		self.assertEqual('USD', currency)

		fixedDeposit = list(fixedDeposit)
		self.assertEqual(9, len(fixedDeposit))
		self.verifyFixedDeposit(fixedDeposit[0])

		bondPositions = list(bondPositions)
		self.assertEqual(7, len(bondPositions))
		self.verifyBondPosition(bondPositions[6])

		cashPositions = list(cashPositions)
		self.assertEqual(1, len(cashPositions))
		self.verifyCashPosition(cashPositions[0])



	def testGetValuationDataFromFile2(self):
		file = join(getCurrentDirectory(), 'samples', 'sample 2021-01-12.xls')
		date, currency, fixedDeposit, bondPositions, cashPositions = \
			getValuationDataFromFile(file)

		self.assertEqual('2021-01-12', date)
		self.assertEqual('USD', currency)

		fixedDeposit = list(fixedDeposit)
		self.assertEqual(24, len(fixedDeposit))
		self.verifyFixedDeposit2(fixedDeposit[23])

		bondPositions = list(bondPositions)
		self.assertEqual(15, len(bondPositions))
		self.verifyBondPosition2(bondPositions[2])

		cashPositions = list(cashPositions)
		self.assertEqual(1, len(cashPositions))
		self.verifyCashPosition2(cashPositions[0])



	def testGetValuationDataFromFile3(self):
		file = join(getCurrentDirectory(), 'samples', 'sample 2021-01-14.xls')
		date, currency, fixedDeposit, bondPositions, cashPositions = \
			getValuationDataFromFile(file)

		self.assertEqual('2021-01-13', date)
		self.assertEqual('USD', currency)

		fixedDeposit = list(fixedDeposit)
		self.assertEqual(24, len(fixedDeposit))

		bondPositions = list(bondPositions)
		self.assertEqual(18, len(bondPositions))
		self.verifyBondPosition3(bondPositions[15])

		cashPositions = list(cashPositions)
		self.assertEqual(1, len(cashPositions))



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



	def verifyFixedDeposit2(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'SHANGHAI PUDONG DEVELOPMENT BANK CO LTD TIME DEPOSIT-USD'
						, p['INVESTMENT'])
		self.assertEqual('', p['ISIN CODE'])
		self.assertEqual('', p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual('', p['AVG UNIT PRICE'])
		self.assertEqual(4500000, p['ORIG CURR BOOK COST'])
		self.assertEqual(4500000, p['PORT CURR BOOK COST'])
		self.assertEqual('', p['MARKET PRICE'])
		self.assertEqual(4500000, p['ORIG CURR MKT VALUE'])
		self.assertEqual(4500000, p['PORT CURR MKT VALUE'])
		self.assertEqual(393.75, p['ACCR INT PORT CCY'])
		self.assertEqual(1.81, p['% OF TOTAL'])
		self.assertEqual(0, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2021-01-08', p['VALUE DATE'])
		self.assertEqual(0.63, p['INT RATE'])
		self.assertEqual('2021-07-09', p['MATURITY DATE'])



	def verifyBondPosition(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'COUNTRY GARDEN HLDGS CO LTD 3.3% S/A 12JAN2031'
						, p['INVESTMENT'])
		self.assertEqual('XS2280833307', p['ISIN CODE'])
		self.assertEqual(4500000, p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual(99.645, p['AVG UNIT PRICE'])
		self.assertEqual(4484025, p['ORIG CURR BOOK COST'])
		self.assertEqual(4484025, p['PORT CURR BOOK COST'])
		self.assertEqual(98.83, p['MARKET PRICE'])
		self.assertEqual(4447350, p['ORIG CURR MKT VALUE'])
		self.assertEqual(4447350, p['PORT CURR MKT VALUE'])
		self.assertEqual('', p['ACCR INT PORT CCY'])
		self.assertEqual(9.08, p['% OF TOTAL'])
		self.assertEqual(-36675.00, p['UNREALIZED P/L PORT CCY']) #-- value modified to fix typo (from -36,675.00 to -36675.00)
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2021-01-05', p['VALUE DATE']) #-- value modified base on sample file (from '2020-01-05' to '2021-01-05')
		self.assertEqual(0, p['INT RATE'])
		self.assertEqual('2031-01-12', p['MATURITY DATE'])



	def verifyBondPosition2(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'CSCEC FINANCE CAYMAN II LTD 2.7% S/A 14JUN2021'
						, p['INVESTMENT'])
		self.assertEqual('XS1430445210', p['ISIN CODE'])
		self.assertEqual(2900000, p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual(100.694, p['AVG UNIT PRICE'])
		self.assertEqual(2920126, p['ORIG CURR BOOK COST'])
		self.assertEqual(2920126, p['PORT CURR BOOK COST'])
		self.assertEqual(100.599, p['MARKET PRICE'])
		self.assertEqual(2917371, p['ORIG CURR MKT VALUE'])
		self.assertEqual(2917371, p['PORT CURR MKT VALUE'])
		self.assertEqual(6307.50, p['ACCR INT PORT CCY'])
		self.assertEqual(1.17, p['% OF TOTAL'])
		self.assertEqual(-2755.00, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2016-06-07', p['VALUE DATE'])
		self.assertEqual(2.7, p['INT RATE'])
		self.assertEqual('2021-06-14', p['MATURITY DATE'])



	def verifyBondPosition3(self, p):
		self.assertEqual(17, len(p))
		self.assertEqual( 'WESTWOOD GROUP HLDGS LTD 4.875% S/A 19APR2021'
						, p['INVESTMENT'])
		self.assertEqual('XS1807198145', p['ISIN CODE'])
		self.assertEqual(5140000, p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual(100.849, p['AVG UNIT PRICE'])
		self.assertEqual(5183638.60, p['ORIG CURR BOOK COST'])
		self.assertEqual(5183638.60, p['PORT CURR BOOK COST'])
		self.assertEqual(100.794, p['MARKET PRICE'])
		self.assertEqual(5180811.60, p['ORIG CURR MKT VALUE'])
		self.assertEqual(5180811.60, p['PORT CURR MKT VALUE'])
		self.assertEqual(59163.54, p['ACCR INT PORT CCY'])
		self.assertEqual(2.08, p['% OF TOTAL'])
		self.assertEqual(-2827.00, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])
		self.assertEqual('2018-04-12', p['VALUE DATE'])
		self.assertEqual(4.875, p['INT RATE'])
		self.assertEqual('2021-04-19', p['MATURITY DATE'])



	def verifyCashPosition(self, p):
		self.assertEqual(14, len(p))
		self.assertEqual( 'USD CASH AC - BANK OF CHINA (HK)'
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
		self.assertEqual(24.29, p['% OF TOTAL'])
		self.assertEqual(0, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])



	def verifyCashPosition2(self, p):
		self.assertEqual(14, len(p))
		self.assertEqual( 'USD CASH AC - BANK OF CHINA (HK)'
						, p['INVESTMENT'])
		self.assertEqual('', p['ISIN CODE'])
		self.assertEqual('', p['NOMINAL QUANTITY'])
		self.assertEqual('USD', p['DEAL CCY'])
		self.assertEqual('', p['AVG UNIT PRICE'])
		self.assertEqual(70831279.39, p['ORIG CURR BOOK COST'])
		self.assertEqual(70831279.39, p['PORT CURR BOOK COST'])
		self.assertEqual('', p['MARKET PRICE'])
		self.assertEqual(70831279.39, p['ORIG CURR MKT VALUE'])
		self.assertEqual(70831279.39, p['PORT CURR MKT VALUE'])
		self.assertEqual('', p['ACCR INT PORT CCY'])
		self.assertEqual(28.46, p['% OF TOTAL'])
		self.assertEqual(0, p['UNREALIZED P/L PORT CCY'])
		self.assertEqual('', p['CLASS CODE'])