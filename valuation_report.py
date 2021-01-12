# # coding=utf-8
# #
# # Functions to read valuation report from BOCI-Prudential valuation
# # report.
# # 
# from os.path import abspath, dirname


# def getValuationDataFromFile(file):
# 	"""
# 	[String] file (daily valuation report for Short Term Bond Fund)
# 		=> [Tuple] ( [String] date (yyyy-mm-dd)
# 				   , [String] portfolio currency
# 				   , [Iterable] fixed deposit positions
# 				   , [Iterable] bond positions
# 				   , [Iterable] bank balance positions
# 				   )
# 	"""
# 	# FIXME: to be implemented
# 	return ('', '', [], [], [])

# """
# 	returns the current directory

# 	for running the test case provided
# """

getCurrentDirectory = lambda : \
    dirname(abspath(__file__))

import os
import sys
from os.path import abspath, dirname, join
from datetime import datetime
# import XlsxWriter
import xlrd
from itertools import tee
import logging
import logging.config
# from itertools import izip

def getValuationDataFromFile(filename):
    return ValuationReport().run(filename)

"""
[String] file (daily valuation report for Short Term Bond Fund)
    => [Tuple] ( [String] date (yyyy-mm-dd)
                , [String] portfolio currency
                , [Iterable] fixed deposit positions
                , [Iterable] bond positions
                , [Iterable] bank balance positions
                )
"""
class ValuationReport:

    def __init__(self):
        logging.config.fileConfig("logging_config.ini",
									defaults={'date':datetime.now().date().strftime('%Y-%m-%d')}
									)
        self.logger = logging.getLogger('sLogger')

    def run(self, file):
        self.logger.info('Running operation on file: ' + file)
        def _group_two_even_row_data(input_dict):
            temp_list = []
            final = []
            #-- group each 2 rows together in nested list
            for i in range(len(input_dict)):
                if (i > 0):
                    temp_list.append(input_dict[i-1])
                if i > 0 and i % 2 == 0:
                    final.append(temp_list)
                    temp_list = []
            return final

        def _data_cleance(input_dict):
            cleanced_dict = [ele for ele in ({key: val for key, val in sub.items() if val} for sub in input_dict) if ele]
            return cleanced_dict

        def _create_iterator(input_list):
                for item in input_list:
                    yield item

        
        #-- variable for currency and date
        portfolio_currency = ""
        portfolio_date = ""

        #-- variable for fixed deposit positions
        fixed_deposit_positions = []
        fixed_deposit_positions_each = dict()
        fixed_deposit_positions_found = 0
        fixed_deposit_positions_start = -1
        row_alt = 0

        #-- variable for bond positions
        bond_positions = []
        bond_positions_each = dict()
        bond_positions_all = []
        bond_positions_found = 0
        bond_positions_start = -1

        #-- variable for bank balance positions
        bank_balance_positions = []
        bank_balance_positions_each = dict()
        bank_balance_positions_found = 0
        bank_balance_positions_start = -1

        #-- open the xls file
        book = xlrd.open_workbook(file)
        worksheet = book.sheet_by_name('Report')
        number_of_rows = worksheet.nrows - 1
        number_of_cols = worksheet.ncols - 1
        #-- setup the column titles
        title_name = ["INVESTMENT", "ISIN CODE", "NOMINAL QUANTITY", "DEAL CCY", "AVG UNIT PRICE", "ORIG CURR BOOK COST", "PORT CURR BOOK COST", "", "MARKET PRICE", "", "ORIG CURR MKT VALUE", "", "PORT CURR MKT VALUE", "", "ACCR INT PORT CCY", "% OF TOTAL", "", "UNREALIZED P/L PORT CCY", "CLASS CODE"]
        title_name_alt = ["INVESTMENT", "ISIN CODE", "VALUE DATE", "INT RATE", "MATURITY DATE", "ORIG CURR BOOK COST", "PORT CURR BOOK COST", "", "MARKET PRICE", "", "ORIG CURR MKT VALUE", "", "PORT CURR MKT VALUE", "", "ACCR INT PORT CCY", "% OF TOTAL", "", "UNREALIZED P/L PORT CCY", "CLASS CODE"]
        
        #-- handling missing sections/data
        section_check = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        section_name = ["Worksheet Title", "Currency", "Fixed Deposit", "Bond", "Liquid Assests & Accruals", "Bank Balance", "Cash Accrual", "BANK DEPOSIT SUBTOTAL", "SUBTOTAL"]
        for r in range(number_of_rows):
            if ("VALUATION OF INVESTMENT" in str(worksheet.row(r)[0])):
                section_check[0] = 1

            if ("Port Currency" in str(worksheet.row(r)[0])):
                section_check[1] = 1

            if ("Fixed Deposit" in str(worksheet.row(r)[0])):
                section_check[2] = 1

            if ("Bond" in str(worksheet.row(r)[0])):
                section_check[3] = 1
            
            if ("Liquid Assests & Accruals" in str(worksheet.row(r)[0])):
                section_check[4] = 1

            if ("Bank Balance" in str(worksheet.row(r)[0])):
                section_check[5] = 1

            if ("Cash Accrual" in str(worksheet.row(r)[0])):
                section_check[6] = 1

        subtotal_count = 0

        #-- check if subtotal rows are present
        for r in range(number_of_rows):
            for c in range(number_of_cols):
                if ("BANK DEPOSIT SUBTOTAL") in str(worksheet.cell_value(r, c)):
                    section_check[7] = 1
                if ("SUBTOTAL") in str(worksheet.cell_value(r, c)):
                    subtotal_count += 1
        if (subtotal_count >= 6):
            section_check[8] = 1
            
        missing_section_message = ""
        if (0 in section_check):
            for i in range(len(section_check)):
                if (section_check[i]) == 0:
                    missing_section_message += section_name[i] + ", "
            if (section_check[8]):
                error_message = "The following data/sections is(are) perhaps incorrect or missing: " + missing_section_message + "please double check the worksheet."
            else:
                error_message = "The following data/sections is(are) perhaps incorrect or missing: " + missing_section_message + "please double check the worksheet. There should be at least 1 occurrence of 'BANK DEPOSIT SUBTOTAL' and 5 occurrences of 'SUBTOTAL'."
            self.logger.error(error_message)
            raise ValueError(error_message)

        #-- for loop ============================================================================
        for r in range(number_of_rows):
            #-- prepare a dictionary for storing each row of data, these reset every loop for each row
            fixed_deposit_positions_each = {}
            bond_positions_each = {}
            bank_balance_positions_each = {}
            for c in range(number_of_cols):

                #-- retrieving portfolio date
                if "VALUATION OF INVESTMENT" in  str(worksheet.cell_value(r, c)):
                    portfolio_date = str(worksheet.cell_value(r, c))
                    portfolio_date = portfolio_date.replace("VALUATION OF INVESTMENT AS AT ", "")
                    portfolio_date = portfolio_date.strip()
                    datetimeobject = datetime.strptime(portfolio_date,'%d %b %Y')
                    portfolio_date = datetimeobject.strftime('%Y-%m-%d')
                    portfolio_date = portfolio_date.strip()

                #-- retrieving portfolio currency
                if "Port Currency" in str(worksheet.cell_value(r, c)):
                    portfolio_currency = str(worksheet.cell_value(r, c))
                    portfolio_currency = portfolio_currency.replace("Port Currency : ", "")
                    portfolio_currency = portfolio_currency.strip()

                #-- dividing sections of the xls file =============================================
                #-- retrieving fixed deposit
                if "Fixed Deposit" in str(worksheet.cell_value(r, c)):
                    fixed_deposit_positions_found = 1
                    fixed_deposit_positions_start = r + 2

                if "Bond" in str(worksheet.cell_value(r, c)):
                    fixed_deposit_positions_found = 0 
                    bond_positions_found = 1
                    bond_positions_start = r + 1

                if "Liquid Assests & Accruals" in str(worksheet.cell_value(r, c)):
                    bond_positions_found = 0

                if "Bank Balance" in str(worksheet.cell_value(r, c)):
                    bond_positions_found = 0
                    bank_balance_positions_found = 1
                    bank_balance_positions_start = r + 1

                #-- break out of the inner for-loop once all required data is found
                if "Cash Accrual" in str(worksheet.cell_value(r, c)):
                    bank_balance_positions_found = 0
                    # print("Found!")
                    # break
                #-- dividing sections of the xls file end =============================================


                #-- retrieving single row fixed deposit positions
                if ((fixed_deposit_positions_found == 1) and (r >= fixed_deposit_positions_start)):
                    if (row_alt == 0):
                        if (title_name[c] != ""):
                            if (c > 14 and c < len(title_name)):
                                if (isinstance(worksheet.cell_value(r, c+1), str)):
                                    try:
                                        fixed_deposit_positions_each[title_name[c]] = worksheet.cell_value(r, c+1).strip()
                                    except ValueError:
                                        self.logger.error("Fixed deposit positions' values invalid")
                                        return    
                                else:
                                    try:
                                        fixed_deposit_positions_each[title_name[c]] = worksheet.cell_value(r, c+1)
                                    except ValueError:
                                        self.logger.error("Fixed deposit positions' values invalid")
                                        return   
                                # print(str(c) + ": " + str(fixed_deposit_positions_each[title_name[c]]) + " | " + str(title_name[c]))
                            else:
                                if (isinstance(worksheet.cell_value(r, c), str)):
                                    try:
                                        fixed_deposit_positions_each[title_name[c]] = worksheet.cell_value(r, c).strip()
                                    except ValueError:
                                        self.logger.error("Fixed deposit positions' values invalid")
                                        return 
                                else:
                                    try:
                                        fixed_deposit_positions_each[title_name[c]] = worksheet.cell_value(r, c)
                                    except ValueError:
                                        self.logger.error("Fixed deposit positions' values invalid")
                                        return 
                                # print(str(c) + ": " + str(fixed_deposit_positions_each[title_name[c]]) + " | " + str(title_name[c]))
                    else:
                        if (worksheet.cell_value(r, c) != '' and worksheet.cell_value(r, c) != '                    ' and c < len(title_name) + 1):
                            fixed_deposit_positions_each[title_name_alt[c]] = worksheet.cell_value(r, c)
                            if title_name_alt[c] == "VALUE DATE" or title_name_alt[c] == "MATURITY DATE":
                                try:
                                    datetimeobject = datetime.strptime(fixed_deposit_positions_each[title_name_alt[c]],'%d/%m/%Y')
                                    fixed_deposit_positions_each[title_name_alt[c]] = datetimeobject.strftime('%Y-%m-%d')
                                except TypeError:
                                    self.logger.error("Fixed deposit positions' values invalid or bond section is missing")
                                    return
                            elif title_name_alt[c] == "INT RATE":
                                try:
                                    fixed_deposit_positions_each[title_name_alt[c]] = float(fixed_deposit_positions_each[title_name_alt[c]].strip('%'))
                                except ValueError:
                                    self.logger.error("Fixed deposit positions' values invalid")
                                    return
                            # print("! " + str(c) + ": " + str(worksheet.cell_value(r, c)) + " | " + str(len(title_name)))     
                
                #-- retrieving single row bond positions
                if ((bond_positions_found == 1) and (r >= 32)):
                    if (title_name[c] != ""):
                        if (c < 15 and c < len(title_name)):
                            if isinstance(worksheet.cell_value(r, c), str):
                                try:
                                    bond_positions_each[title_name[c]] = worksheet.cell_value(r, c).strip()
                                except ValueError:
                                    self.logger.error("bond positions' values invalid")
                                    return
                            else:
                                try:
                                    bond_positions_each[title_name[c]] = worksheet.cell_value(r, c)
                                except ValueError:
                                    self.logger.error("bond positions' values invalid")
                                    return
                        else:
                            if isinstance(worksheet.cell_value(r, c+1), str):
                                try:
                                    bond_positions_each[title_name[c]] = worksheet.cell_value(r, c+1).strip()
                                except ValueError:
                                    self.logger.error("bond positions' values invalid")
                                    return
                            else:
                                try:
                                    bond_positions_each[title_name[c]] = worksheet.cell_value(r, c+1)
                                except ValueError:
                                    self.logger.error("bond positions' values invalid")
                                    return


                #-- retrieving single row bank balance positions
                if ((bank_balance_positions_found == 1) and (r >= bank_balance_positions_start)):
                    
                    if (c < 15 and c < len(title_name)):
                        try:
                        # print(worksheet.cell_value(r, c))
                            bank_balance_positions_each[title_name[c]] = worksheet.cell_value(r, c)
                        except ValueError:
                            self.logger.error("bank balance positions' values invalid")
                            return
                    else:
                        try:
                            # print(worksheet.cell_value(r, c))
                            bank_balance_positions_each[title_name[c]] = worksheet.cell_value(r, c-1)
                        except ValueError:
                            self.logger.error("bank balance positions' values invalid")
                            return
                    
                    bank_balance_positions_each[title_name[c]] = worksheet.cell_value(r, c)

            #-- alternate the title of the rows as some data has 2 rows of info
            if (row_alt == 0):
                row_alt = 1
            else:
                row_alt = 0

            #-- collect fixed deposit positions
            if (fixed_deposit_positions_found == 1):
                fixed_deposit_positions.append(fixed_deposit_positions_each)

            #-- collect bond positions
            if (bond_positions_found == 1):
                if (bond_positions_each.get("NOMINAL QUANTITY") != ''):
                    row_alt_start = 1
                    bond_positions_all.append(bond_positions_each)

            #-- collect bank balance positions    
            if (bank_balance_positions_found == 1):   
                if (bond_positions_each.get("INVESTMENT") != ''):
                    bank_balance_positions.append(bank_balance_positions_each)
    
        #-- for loop end ========================================================================

        #-- bond position post processing =======================================================
        bond_positions_cleanced = list(filter(None, bond_positions_all))
        for i in range(len(bond_positions_cleanced)):
            #-- manipulate the alternating row of data
            if (i % 2 != 0):
                #-- update the key with the alternate titles as well as formatting the dates
                VALUE_DATE = bond_positions_cleanced[i].get("NOMINAL QUANTITY")
                INT_RATE = float(bond_positions_cleanced[i].get("DEAL CCY").strip('%'))
                MATURITY_DATE = bond_positions_cleanced[i].get("AVG UNIT PRICE")
                bond_positions_cleanced[i].clear()

                datetimeobject = datetime.strptime(VALUE_DATE,'%d/%m/%Y')
                VALUE_DATE = datetimeobject.strftime('%Y-%m-%d')

                datetimeobject = datetime.strptime(MATURITY_DATE,'%d/%m/%Y')
                MATURITY_DATE = datetimeobject.strftime('%Y-%m-%d')

                bond_positions_cleanced[i]['VALUE DATE'] = VALUE_DATE
                bond_positions_cleanced[i]['INT RATE'] = INT_RATE
                bond_positions_cleanced[i]['MATURITY DATE'] = MATURITY_DATE
        #-- divide the dictionary into chunks of 2, then merged each chunk of 2 into one single line of data
        bond_positions_merged_combined = list(zip(*[iter(bond_positions_cleanced)]*2))
        final_bond_positions_merged = []
        for i in range(len(bond_positions_merged_combined)):
            final_bond_positions_merged.append({**bond_positions_merged_combined[i][0], **bond_positions_merged_combined[i][1]})
        #-- =====================================================================================  

        #-- fixed deposit positions post processing =============================================
        final_fixed_deposit_positions = _group_two_even_row_data(fixed_deposit_positions)
        final_fixed_deposit_positions_merged = []
        for i in range(len(final_fixed_deposit_positions)):
            final_fixed_deposit_positions_merged.append({**final_fixed_deposit_positions[i][0], **final_fixed_deposit_positions[i][1]})
        try:
            final_fixed_deposit_positions_merged.pop(0)
            final_fixed_deposit_positions_merged.pop(len(final_fixed_deposit_positions_merged)-1)
        #-- ===================================================================================== 

        #-- bank balance positions post processing ==============================================
        #-- remove the data of header row, total value row as well as spacing row
            bank_balance_positions.pop(0)
            bank_balance_positions.pop(len(bank_balance_positions)-1)
            bank_balance_positions.pop(len(bank_balance_positions)-1)
        except IndexError:
            error_message = "Operation error on bank balance section, perhaps certain section or sub total is missing?"
            self.logger.error(error_message)
            raise IndexError(error_message)
        except KeyError:
            error_message = "Operation error on bank balance section, perhaps certain section or sub total is missing?"
            self.logger.error(error_message)
            raise KeyError(error_message)
        
        #-- fixing some missed placed data to their right key
        for i in range(len(bank_balance_positions)):
            bank_balance_positions[i]['% OF TOTAL'] = bank_balance_positions[i].get('')
            bank_balance_positions[i].pop('')
            temp = bank_balance_positions[i].get('UNREALIZED P/L PORT CCY')
            bank_balance_positions[i]['UNREALIZED P/L PORT CCY'] = bank_balance_positions[i].get('CLASS CODE')
            bank_balance_positions[i]['CLASS CODE'] = temp
        #-- ===================================================================================== 

        #-- create iterators===================================================================== 
        final_fixed_deposit_positions = _create_iterator(final_fixed_deposit_positions_merged)
        final_bond_positions = _create_iterator(final_bond_positions_merged)
        final_bank_balance_positions = _create_iterator(bank_balance_positions)
        output_tuple = (portfolio_date, portfolio_currency, final_fixed_deposit_positions, final_bond_positions, final_bank_balance_positions)
        #-- =====================================================================================
        if portfolio_currency == '':
            error_message = "Currency of the report not found, please check if you have included the currency as 'Port Currency : xxx'"
            self.logger.error(error_message)
            raise ValueError(error_message)

        if portfolio_date == '':
            error_message = "Date not found, please check if the title of the worksheet is correct."
            self.logger.error(error_message)
            raise ValueError(error_message)

        self.logger.info('valuation_report operation completed!')
        return (output_tuple)
