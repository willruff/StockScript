from textx import metamodel_from_file
from stock import Stock
from crypto import Crypto
from marketSimulator import MarketSimulator
import sys

class StockScriptInterpreter:
    def __init__(self):
        self.assets = {}
        self.simulator = MarketSimulator()

    def execute(self, model):
        # loop through statements and check each statement type to call the correct method
        for stmt in model.statements:
            if stmt.__class__.__name__ == 'StockDeclaration':
                self.declare_stock(stmt)
            elif stmt.__class__.__name__ == 'CryptoDeclaration':
                self.declare_crypto(stmt)
            elif stmt.__class__.__name__ == 'AssetOperation':
                self.operate_asset(stmt)
            elif stmt.__class__.__name__ == 'Display':
                self.handle_display(stmt)
            elif stmt.__class__.__name__ in ['SimulateMarket', 'SimulateAsset']:
                self.handle_simulation(stmt)

    # create stock and add to assests dict
    def declare_stock(self, stmt):
        stock = Stock(stmt.name, stmt.price, stmt.shares)
        self.assets[stmt.name] = stock

    # create crypto coin and add to asses dict
    def declare_crypto(self, stmt):
        crypto = Crypto(stmt.name, stmt.price, stmt.supply)
        self.assets[stmt.name] = crypto

    # operations for stocks and crypto
    def operate_asset(self, stmt):
        # get stock or crypto from dict to be operated on
        asset = self.assets.get(stmt.asset.name)
        if not asset:
            raise ValueError(f"Asset '{stmt.asset.name}' not found.")
        
        # get the operation type (ex. adjust_price, merge, etc)
        operation = getattr(asset, stmt.operation, None)
        if not operation:
            raise ValueError(f"Operation '{stmt.operation}' not supported.")

        # checks if the input to the operation is a parameter, this means stock will be doing merge
        if hasattr(stmt.parameter, 'asset') and stmt.parameter.asset is not None:
            # get the other stock or cryptos value
            other_asset = self.assets.get(stmt.parameter.asset.name)
            if not other_asset:
                raise ValueError(f"Asset '{stmt.parameter.asset.name}' not found for operation '{stmt.operation}'.")
            # execute merge operation
            operation(other_asset)
            # delete the old stock or crypto from the dict/state
            del self.assets[stmt.parameter.asset.name]
        else:
            # do the other non merging operations
            operation(stmt.parameter)

    def handle_display(self, stmt):
        # get display type. all happens if user calls only "display"
        display_type = stmt.displayType if stmt.displayType is not None else 'all'
        
        if stmt.asset is None:  # display all assets
            stocks = []
            cryptos = []
            
            # separate stocks and cryptos for printing
            for name, asset in self.assets.items():
                if isinstance(asset, Stock):
                    stocks.append(asset)
                elif isinstance(asset, Crypto):
                    cryptos.append(asset)
            
            # sort in alphabetical order
            stocks.sort(key=lambda x: x.name)
            cryptos.sort(key=lambda x: x.name)
            
            print("\n=== Asset Summary ===")
            print(f"Total Assets: {len(self.assets)}")
            print(f"Stocks: {len(stocks)}")
            print(f"Cryptocurrencies: {len(cryptos)}")
            print("====================\n")
            
            # print stocks
            if stocks:
                print("   === Stocks ===")
                for stock in stocks:
                    print("-" * 20)
                    stock.display(display_type)

            # print crypto  
            if cryptos:
                print("\n=== Cryptocurrencies ===")
                for crypto in cryptos:
                    print("-" * 20)
                    crypto.display(display_type)
            print("====================\n")
        else:  # Display specific asset
            # get specific stock or crypto class from state
            asset = self.assets.get(stmt.asset.name)
            if not asset:
                raise ValueError(f"Asset '{stmt.asset.name}' not found.")
            asset.display(display_type)

    def handle_simulation(self, stmt):
        # get sentiment directly (ex. good_day, bad_day, etc)
        sentiment = stmt.sentiment.type
        if sentiment not in ['good_day', 'bad_day', 'random_day']:
            raise ValueError(f"Invalid sentiment type: {sentiment}")

        # check if user wants to simulate market or asset
        if stmt.__class__.__name__ == 'SimulateMarket':
        # market-wide simulation
            print(f"\n=== Simulating {sentiment} for entire market ===")
            
            # loop through all assets and make proper changes to values
            for name, asset in self.assets.items():
                is_crypto = isinstance(asset, Crypto)
                # calls random change to make outputs vary
                base_change = self.simulator.get_random_change(sentiment, is_crypto)
                # applys extra individual change to make market more random
                final_change = self.simulator.apply_individual_variation(base_change)
                
                # apply changes to the assets
                old_price = asset.price
                percent_change = final_change / 100
                asset.price *= (1 + percent_change)
                asset.marketCap = asset.price * (asset.shares if isinstance(asset, Stock) else asset.supply)
                
                # print the applied changes
                print(f"{name}: ${old_price:.2f} → ${asset.price:.2f} ({final_change:+.2f}%)")
        else:
            # Individual asset simulation
            asset = self.assets.get(stmt.asset.name)
            if not asset:
                raise ValueError(f"Asset '{stmt.asset.name}' not found.")
            
            # calling functions for specific asset
            is_crypto = isinstance(asset, Crypto)
            base_change = self.simulator.get_random_change(sentiment, is_crypto)
            final_change = self.simulator.apply_individual_variation(base_change)
            
            # apply changes to the asset
            old_price = asset.price
            percent_change = final_change / 100
            asset.price *= (1 + percent_change)
            asset.marketCap = asset.price * (asset.shares if isinstance(asset, Stock) else asset.supply)
            
            # print simulation type and outcome
            print(f"\nSimulated {sentiment} for {stmt.asset.name}")
            print(f"Price changed: ${old_price:.2f} → ${asset.price:.2f} ({final_change:+.2f}%)")

if __name__ == "__main__":
    fileName = sys.argv[1]
    try:
        # load the grammar
        asset_mm = metamodel_from_file("stock.tx")

        # parse the program
        asset_model = asset_mm.model_from_file(fileName)

        # execute the program
        interpreter = StockScriptInterpreter()
        interpreter.execute(asset_model)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()