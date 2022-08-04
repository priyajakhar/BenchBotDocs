import pandas as pd, openpyxl
 
# opening the main sheet in read mode
df  = pd.read_excel('main.xlsx')
 
# getting row counts
colvalues = df[['rows']].values
i = 0
rarr = [None] * colvalues.size
for num in colvalues:
   rarr[i] = num[0]
   i = i+1
 
# getting species names
species = df[['species']].values
i = 0
sarr = [None] * species.size
for num in species:
   sarr[i] = num[0]
   i = i+1
 
# opening the secondary sheet in write mode
wb = openpyxl.load_workbook('weeds.xlsx')
sheet = wb.active
 
s = 0
for rownums in rarr:
   species_row = [int(e) for e in rownums.split(',')]
   for val in species_row:
       nam = str(species[s])[2:-2]
       sheet.cell(row = val+1, column = 1).value = nam
   s+= 1
 
wb.save('weeds.xlsx')
