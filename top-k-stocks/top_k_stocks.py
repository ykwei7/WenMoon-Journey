import csv

def top_k_stocks(k):
    stocks = []
    with open("nasdaq_screener.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        notFirstRow = True
        for row in reader:
            if not notFirstRow and row[5] != "":
                stocks.append({"Name": row[0], "MktCap": int(float(row[5]))})
            notFirstRow = False

    stocks = sorted(stocks, key=lambda i: i['MktCap'], reverse=True)[0:k]

    with open(f"top-{k}-stocks.csv", "w") as f:
        for x in stocks:
            txt = "\"{name},{mktcap}\"\n".format(name=x["Name"], mktcap=x["MktCap"])
            f.writelines(txt)

