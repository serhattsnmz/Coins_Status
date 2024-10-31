from prettytable import PrettyTable
import requests
import json
import os
import argparse
import platform

class LastCoinApi:
    def __init__(self):
        self.binanceUrl = "https://api.binance.com/api/v1/ticker/24hr?symbol="
        self.binanceSymbols = ["BTCUSDT", "ETHUSDT","XVGBTC", "BNBBTC"]

        self.btcTurkUrl = "https://api.btcturk.com/api/v2/ticker?pairSymbol="
        self.btcTurkSymbols = ["BTCUSDT", "ETHUSDT"]

    def clear(self):
        try:
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
        except:
            pass

    def binance_create_request(self, symbol):
        req = requests.get(self.binanceUrl + symbol)
        return json.loads(req.content)
    
    def btcTurk_create_request(self, symbol):
        req = requests.get(self.btcTurkUrl + symbol)
        return req.json().get("data")

    def binance_values(self):
        table = PrettyTable(["Symbol", "Last Price", "HIGH", "LOW"])
        for symbol in self.binanceSymbols:
            js = self.binance_create_request(symbol)
            table.add_row([js["symbol"],js["lastPrice"],js["highPrice"],js["lowPrice"]])
        self.binanceTable = table

    def btcTurkValues(self):
        table = PrettyTable(["Symbol", "Last Price", "Average", "HIGH", "LOW"])
        for symbol in self.btcTurkSymbols:
            js = self.btcTurk_create_request(symbol)
            table.add_row([js[0]["pair"],js[0]["last"],js[0]["average"],js[0]["high"],js[0]["low"]])
        self.btcTurkTable = table

    def write_values(self):
        self.btcTurkValues()
        self.binance_values()
        self.clear()
        print("BTCTURK.COM")
        print(self.btcTurkTable)
        print("BINANCE.COM")
        print(self.binanceTable)

def parse_args():
    parser = argparse.ArgumentParser(description="Get Coins Values")
    parser.add_argument("-t", "--type", choices=["single","infinite"], default="single", metavar="", help="Use that for infinite loop. Choices : 'single'(default) or 'infinite'")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    api  = LastCoinApi()

    if args.type == "infinite": 
        try:
            time = 1
            while True:
                api.write_values()
                print("Total Request:", time, "- Quit: Ctrl+C")
                time += 1
        except KeyboardInterrupt:
            pass
    else:
        api.write_values()
