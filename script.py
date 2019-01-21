import csv
from Venter . models import Organisation, Header

with open('/Users/sndtcsi/Venter_CMS/MEDIA/demoicmc/CSV/input/demoicmc.csv', mode = 'r') as csv_file:
	reader = csv.reader(csv_file)
    # row 1 contains all the column names of the first row of the csv file uploaded
	row1 = next(reader)

# strip() function to be executed over each item of row1 (a list) to remove all the leading and trailing whitespaces from each item of the list 
strip_list_from_row1 = [item.strip() for item in row1]

# converting 'strip_list_from_row1' from a list to a set called 'set_of_row1'
set_of_row1 = set(strip_list_from_row1)

# retrieve organisation name
org_name = Organisation.objects.get(organisation_name = 'ICMC') # pylint: disable = E1101

# retrieve headers list for particular organisation
model_header_list = Header.objects.filter(organisation_name = org_name).values_list('header', flat=True) # pylint: disable = E1101

# convert list to set 'c'
c = set(model_header_list) 

# header validation of the two sets
set_of_row1 ==  c # returns True