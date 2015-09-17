# Robinhood
Python Framework to make trades with Robinhood Private API
Forked from https://github.com/itsff/Robinhood

##Current Features 
- Placing buy orders (Robinhood.place_buy_order)
- Placing sell order (Robinhood.place_sell_order)
- Quote Information (Robinhood.quote_data)
- Account Information (Robinhood.account)
- Portfolio Information (Robinhood.portfolio)
- More coming soon

###How To Install:
    pip install -r requirements.txt

###How to Use (see [example.py](https://github.com/dsouzarc/Robinhood/blob/master/example.py))
  from Robinhood import Robinhood
  my_trader = Robinhood(username="USERNAME HERE", password="PASSWORD HERE")
  stock_instrument = my_trader.instruments("GEVO")[0]
  quote_info = my_trader.quote_data("GEVO")
  buy_order = my_trader.place_buy_order(stock_instrument, 1)
  sell_order = my_trader.place_sell_order(stock_instrument, 1)

####Data returned
+ Ask Price
+ Ask Size
+ Bid Price
+ Bid Size
+ Last trade price
+ Previous close
+ Previous close date
+ Adjusted previous close
+ Trading halted
+ Updated at
