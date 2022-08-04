import pandas as pd, openpyxl

#reading content of main file
df  = pd.read_excel('main.xlsx')
count = df[['pics to take']].values
pics = [None] * count.size
i = 0
for num in count:
    pics[i] = num[0]
    i = i+1

names = df[['species']].values
weed = [None] * names.size
i = 0
for name in names:
    weed[i] = name[0]
    i = i+1

#reading weedlist in secondary file
file = "weeds.xlsx"
rb  = pd.read_excel(file)
species = rb[['species']].values

#saving the file after updates
wb = openpyxl.load_workbook(file) 
sheet = wb.active
i = 0
for sp in species:
    idx = weed.index(sp[0])
    cnt = pics[idx]
    sheet.cell(row=i+2, column=2).value=cnt
    i = i+1

wb.save(file)
