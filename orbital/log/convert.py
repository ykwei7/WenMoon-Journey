import csv

stocks = []

with open("stocks_log-21072021.csv", "r") as f:
    reader = csv.reader(f)
    for x in reader:
        stocks.append(x)

def make_row(lst):
    str = "<tr>\n \t"
    for x in lst:
        str += "<td>" + x + "</td>"
        str += "\n \t"
    str += "</tr>"
    return str

for x in stocks:
    print(make_row(x))
