import json
import requests
import urllib
from collections import OrderedDict

class Robinhood:

    session = None

    username = None

    password = None

    headers = None

    auth_token = None

    data = {        
        'account_number': None
    }

    url = None

    endpoints = {
            "login": "https://api.robinhood.com/api-token-auth/",
            "investment_profile": "https://api.robinhood.com/user/investment_profile/",
            "accounts":"https://api.robinhood.com/accounts/",
            "ach_iav_auth":"https://api.robinhood.com/ach/iav/auth/",
            "ach_relationships":"https://api.robinhood.com/ach/relationships/",
            "ach_transfers":"https://api.robinhood.com/ach/transfers/",
            "applications":"https://api.robinhood.com/applications/",
            "dividends":"https://api.robinhood.com/dividends/",
            "edocuments":"https://api.robinhood.com/documents/",
            "instruments":"https://api.robinhood.com/instruments/",
            "margin_upgrades":"https://api.robinhood.com/margin/upgrades/",
            "markets":"https://api.robinhood.com/markets/",
            "notifications":"https://api.robinhood.com/notifications/",
            "orders":"https://api.robinhood.com/orders/",
            "password_reset":"https://api.robinhood.com/password_reset/request/",
            "quotes":"https://api.robinhood.com/quotes/",
            "document_requests":"https://api.robinhood.com/upload/document_requests/",
            "user":"https://api.robinhood.com/user/",
            "watchlists":"https://api.robinhood.com/watchlists/"
    }

    ##############################
    #Logging in and initializing
    ##############################

    def __init__(self, username, password):
        self.session = requests.session()
        self.session.proxies = urllib.getproxies()
        self.username = username
        self.password = password
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
        }
        self.session.headers = self.headers
        self.login()
        self.accounts()
        self.portfolio()
        self.holdings()

    def login(self):
        data = "password=%s&username=%s" % (self.password, self.username)
        res = self.session.post(self.endpoints['login'], data=data)
        res = res.json()
        self.auth_token = res['token']
        self.headers['Authorization'] = 'Token '+self.auth_token


    ##############################
    # USER DATA 
    ##############################

    def accounts(self):
        accounts = self.session.get(self.endpoints['accounts'])
        self.url = accounts.json()['results'][0]['url']
        self.data['account_number'] = accounts.json()['results'][0]['account_number']
        self.data['buying_power'] = float(accounts.json()['results'][0]['buying_power'])
        return accounts

    def user(self):
        return self.session.get(self.endpoints['user'])

    ##############################
    # PORTFOLIO DATA 
    ##############################

    def investment_profile(self):
        return self.session.get(self.endpoints['investment_profile'])   

    def portfolio(self):
        portfolio = self.session.get(self.url+"portfolio/")
        self.data['portfolio_current_value'] = float(portfolio.json()['market_value'])
        return portfolio

    def holdings(self):
        holdings = self.session.get(self.url+"positions/")
        self.data['holdings'] = []
        total = 0
        for holding in holdings.json()['results']:
            instrument = self.session.get(holding['instrument']).json()
            price = float(self.bid_price(instrument['symbol']))
            newHolding = {
                'symbol': instrument['symbol'],
                'name': instrument['name'],
                'purchase_price': holding['average_buy_price'],
                'current_price': price,
                'current_value': float(holding['quantity']) * price,               
                'shares': holding['quantity'],
                'percent': 0
            }
            self.data['holdings'].append(newHolding)
            total += newHolding['current_value']

        for holding in self.data['holdings']:
            if total > 0:
                holding['percent'] = holding['current_value'] / total
            else:
                holding['percent'] = 0

        return holdings

    def dividends(self):
        return self.session.get(self.endpoints['dividends'])

    def get_allocations(self):
        allocations = OrderedDict()
        for holding in self.data['holdings']:
            allocations[str(holding['symbol'])] = holding['percent']  # symbols and corresponding allocations
        return allocations

    def print_porfolio_header(self):
        print '*** Porfolio ***'
        print 'Current Value: ' + str(self.data['portfolio_current_value']) + ' Buying Power: ' + str(self.data['buying_power'])

    def print_holdings(self):
        print "*** Holdings ***"
        for holding in self.data['holdings']:
            print holding['name'] + ' (' + holding['symbol'] + ')' + ' Shares: ' + holding['shares'] + ' Purchase Price: ' + holding['purchase_price']


    ##############################
    # STOCK DATA 
    ##############################

    def instruments(self, stock=None):
        res = self.session.get(self.endpoints['instruments'], params={'query':stock.upper()})
        res = res.json()
        return res['results'] 

    def quote_data(self, stock=None):
        #Prompt for stock if not entered
        if stock is None:
            stock = raw_input("Symbol: ");
        url = str(self.endpoints['quotes']) + str(stock) + "/"
        #Check for validity of symbol
        try:
            res = json.loads((urllib.urlopen(url)).read());
            if len(res) > 0:
                return res;
            else:
                raise NameError("Invalid Symbol: " + stock);
        except (ValueError):
            raise NameError("Invalid Symbol: " + stock);

    def get_quote(self, stock=None):
        data = self.quote_data(stock)
        return data

    def ask_price(self, stock=None):
        return self.quote_data(stock)['ask_price'];

    def ask_size(self, stock=None):
        return self.quote_data(stock)['ask_size'];

    def bid_price(self, stock=None):
        return self.quote_data(stock)['bid_price'];

    def bid_size(self, stock=None):
        return self.quote_data(stock)['bid_size'];

    def last_trade_price(self, stock=None):
        return self.quote_data(stock)['last_trade_price'];

    def last_trade_price(self, stock=None):
        return self.quote_data(stock)['last_trade_price'];

    def previous_close(self, stock=None):
        return self.quote_data(stock)['previous_close'];

    def previous_close_date(self, stock=None):
        return self.quote_data(stock)['previous_close_date'];

    def adjusted_previous_close(self, stock=None):
        return self.quote_data(stock)['adjusted_previous_close'];

    def symbol(self, stock=None):
        return self.quote_data(stock)['symbol'];

    def last_updated_at(self, stock=None):
        return self.quote_data(stock)['updated_at'];

    def print_quote(self, stock=None):
        data = self.quote_data(stock)
        print(data["symbol"] + ": $" + data["last_trade_price"]);

    def print_quotes(self, stocks):
        for i in range(len(stocks)):
            self.print_quote(stocks[i]);


    ##############################
    #PLACE ORDER
    ##############################

    def place_order(self, symbol, quantity=1, bid_price = None, transaction=None):
        quotes = self.instruments(symbol)
        if(len(quotes) == 0):
            return []
        
        instrument = quotes[0]

        if bid_price == None:
            bid_price = self.quote_data(instrument['symbol'])[0]['bid_price']
        data = 'account=%s&instrument=%s&price=%f&quantity=%d&side=buy&symbol=%s&time_in_force=gfd&trigger=immediate&type=market' % (urllib.quote('https://api.robinhood.com/accounts/'+self.data['account_number']+'/'), urllib.unquote(instrument['url']), float(bid_price), quantity, instrument['symbol']) 
        res = self.session.post(self.endpoints['orders'], data=data)
        return res

    def place_buy_order(self, symbol, quantity, bid_price=None):
        transaction = "buy"
        return self.place_order(symbol, quantity, bid_price, transaction)

    def place_sell_order(self, symbol, quantity, bid_price=None):
        transaction = "sell"
        return self.place_order(symbol, quantity, bid_price, transaction)
