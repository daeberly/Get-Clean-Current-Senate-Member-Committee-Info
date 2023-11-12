# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:20:59 2023

@author: deberly
"""

import pandas as pd
import time
start = time.time()

# Use results from Power Automate webscrape
## 
file = 'Senate_Member_CommitteeAssignments.xlsx'
raw_data = pd.read_excel( file )

#%% 
#
# Rename columns to help manipulate data
#

## Why? The first row is the first member'?

# Shift column names down to be the first row of data
temp = raw_data
temp.loc[-1] = temp.columns.values
temp.sort_index(inplace=True)
temp.reset_index(drop=True, inplace=True)

# Rename columns
    # Get column names
col_names = temp.columns.to_list()
    # New column names
new_col_names = ['temp', 'delete', 'website']
    # Make a dictionary  {"current name": "new name", etc...}
dictionary= dict(zip(col_names, new_col_names))
#print(dictionary)
    # Rename column names
temp = temp.rename( columns = dictionary )

#%%

#
# Remove unwanted column & rows
#

# Remove/Drop unneccessary column
temp = temp.drop(columns='delete')

# Filter out rows with "Back to top"
    # Get 3rd row value in 1st column with "back to top". 3rd row index = 2
cell_value = temp['temp'].iloc[2]
    # Get rows that do NOT equal (filter out)
temp_filtered = temp[temp['temp'] != cell_value]

#
# Get name & website
#

# Get subset of data to store full name
    # Filter out rows with blank cells 
temp__names_websites = temp_filtered[temp_filtered['website'].notnull()]

    # Rename columns
update = {'temp':'ListingName'} 
temp__names_websites = temp__names_websites.rename( columns = update )
temp__names_websites.reset_index(inplace = True, drop = True)


#
# Start building final spreadsheet
#
    # Set name as index to add everything to later
final = temp__names_websites
#final = final.set_index(['ListingName'])

#%%

#
# Get Political Party & State
#
    # Split nama column to get Political Party & State
temp_party_state = temp__names_websites
temp_party_state = temp_party_state.drop(columns='website').squeeze()
    # Split out Politcal Party
tempB= temp_party_state.str.split('(', expand= True)
    # Split out State
tempB= tempB[1].str.split('-', expand= True)
tempB[1] = tempB[1].str.replace(')', '')
    # Rename columns & add to final
update = {0:'Party', 1:'State'} 
tempB = tempB.rename( columns = update )
            # Add to final product
final = final.join(tempB['Party'])
final = final.join(tempB['State'])
#%%

#
# Get/Clean committee & subcommittee assignments
#

# Why? one cell contains all the committees and subcommittees listed
# for each member. But is in the cell below and not helpful that way.

    # Get rows with committee assignments
temp_committees = temp_filtered[temp_filtered['website'].isna()]
temp_committees.reset_index(inplace = True, drop = True)

    # Clean hidden characters in cell
#print(temp_committees.sample(1))
# Result: 94  \n\n\nCommittee on Agriculture, Nutrition, and...     NaN
temp_committees['temp'] = temp_committees['temp'].str.replace('\n', '')

    # Add a delimiter to help split cell data 
temp_committees['temp'] = temp_committees['temp'].str.replace('Committee', '|Committee')
temp_committees['temp'] = temp_committees['temp'].str.replace('Subcommittee', '|Subcommittee')
temp_committees['temp'] = temp_committees['temp'].str.replace('Commission', '|Commission')
#print(temp_committees.sample(20))

    # Break up cell based on committee or commission
        # Committees
            # Convert to Series in order to split cell data
tempA = temp_committees['temp'].squeeze()
#print(type(tempA))
            # Split on delimited " | "
tempA = tempA.str.split(r'|', expand= True ) # Shifts from series to dataframe when cell text expands to multiple columns
tempA = tempA.drop(columns= 0)

### Wanted to regroup by Committee, subcommittee and commission

# A bridge too far for this quick effort

###
            # Create list of committees & 
mbr_committees = tempA.stack().groupby(level=0).apply('; '.join).to_frame()

            # Rename columns
update = {0:'committees'} 
mbr_committees = mbr_committees.rename( columns = update )
            # Add to final product
final = final.join(mbr_committees['committees'])
#%%

# Add column whether senate or house
final.loc[final['website'].str.contains('senate'), 'congress'] = 'senate'
final.loc[final['website'].str.contains('house'), 'congress'] = 'house'

# Is a ranking member on a committee?
final.loc[final['committees'].str.contains('Ranking'), 'ranking_member'] = 'Yes'

# Is a chairman or cochair on a committee?
final.loc[final['committees'].str.contains('Chairman'), 'chairman'] = 'Yes'
final.loc[final['committees'].str.contains('Cochairman'), 'chairman'] = 'Yes'

#%%

## Export
new_file_name = 'senate_member_committees'
final.to_excel( new_file_name + '.xlsx', index= False)


## Admin
end = time.time()
total_time = round(end-start, 2)

print('Total processing time: ', str(total_time), ' seconds.')
