# Define Error Logging
def printerror(ex):
	print('\033[31m'  + str(ex) + '\033[0m', flush=True)

def printwarning(warn):
	print('\033[33m' + str(warn) + '\033[0m', flush=True)

def printyellow(warn) -> str:
	return('\033[33m' + str(warn) + '\033[0m')

def printgreen(msg) -> str:
	return('\033[32m' + str(msg) + '\033[0m')

def printblue(msg) -> str:
	return('\033[34m' + str(msg) + '\033[0m')


import os
try:
	from pathlib import Path
	import rispy
	import traceback
	import re
except ModuleNotFoundError as ex:
	printerror("The app could not be started, a module is missing.")
	printerror("Please run command pip install -r requirements.txt")
	printerror(ex)
	exit(2)
except Exception as ex:
	printerror("An unknown error occured while loading modules." + str(ex))
	exit(2)

def importRis(filepath: str) -> list[dict]:
	p = Path(filepath)

	# Overwrite rispy default list, as rispy only works with one url per document
	try:
		rispy.LIST_TYPE_TAGS.extend(["UR", "M1", "L1", "L2"])
		entries = rispy.load(p, encoding='utf-8')
		print("Detected " + printblue(str(len(entries))) + " items in ris file.")
		return entries
	except OSError as e:
		printerror("RIS is not properly formatted, probably missing article type.")
		printerror(traceback.format_exc())
		return None
	except Exception as e:
		printerror(str(e))
		printerror(traceback.format_exc())
		return None

if __name__ == "__main__":
# Get filepath to RIS file
	("Enter all filepaths of RIS files. If no ore files, leave blank and press enter.")
	filepathOriginal = ""
	filepaths = []
	while not filepathOriginal:
		filepathOriginal = input("Enter full filepath to .ris file: ")
		if filepathOriginal == "":
			break
		# Test if input starts with " and remove
		if filepathOriginal.startswith('"'):
			filepathOriginal = filepathOriginal[1:]
		# Test if abstract ends with 
		if filepathOriginal.endswith('"'):
			filepathOriginal = filepathOriginal[:-1]
		# Test if file exist
		if not os.path.exists(filepathOriginal):
			printerror("File does not exist!")
			filepathOriginal = None
			continue
		# Check if it is a .ris file
		if not filepathOriginal.endswith('.ris'):
			printerror("Given file is not a .ris file!")
			filepathOriginal = None
		filepaths.append(filepathOriginal)
		filepathOriginal = None

	print("Detected " + str(len(filepaths)) + " RIS files.")

	entries = []
	for ris in filepaths:
		result = (importRis(ris))
		entries.extend(result)
	if entries == None:
		printwarning("No results found, will exit.")
		exit(4)
	totalCount = len(entries)

	try:
		# Count Years
		maxyear = 0
		for item in entries:
			if 'year' in item:
				item['year'] = re.sub("[^0-9]", "", item['year'])
				if int(item['year']) > maxyear:
					maxyear = int(item['year'])
		minyear = maxyear
		
		typelist = {}
		for item in entries:	
			if 'year' in item:
				if int(item["year"]) < minyear:
					minyear = int(item["year"])
			if 'type_of_reference' in item:
				typelist[item['type_of_reference']] = 0

		print("Max Year:", str(maxyear))
		print("Min Year:", str(minyear))

		yearlist = {}
		current = minyear
		while current <= maxyear:
			yearlist[current] = 0
			current +=1

		itemswithoutyear: int = 0
		itemswithouttype: int = 0
		for item in entries:
			for year in yearlist:
				if "year" in item:
					if int(item["year"]) == year:
						yearlist[year] +=1
				else:
					itemswithoutyear +=1
			for type in typelist:
				if "type_of_reference" in item:
					if item["type_of_reference"] == type:
						typelist[type] +=1
				else:
					itemswithouttype +=1

	except Exception as ex:
		printerror("An error occured: " + str(ex))
		printerror(traceback.format_exc())

	print("Years: " + str(yearlist))
	print("Document types: " + str(typelist))
	print("Items without year:", itemswithoutyear)
	print("Items without document type:" , itemswithouttype)
	input("Press any key to exit.")