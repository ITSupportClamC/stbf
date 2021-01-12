import sys
import os
from valuation_report import ValuationReport

def main():
    # print command line arguments
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        ValuationReport().run(filepath)
    else:
        print_menu()

def print_menu():
	print("To Run Program               : python -m stbf <workbook_filenpath>")
	print("Sample Run                   : python -m stbf \"samples\\sample InvestValSTBF.xls\" ")
	print("")
	print("To Run Unittest              : python -m unittest2")

if __name__ == "__main__":
    main()