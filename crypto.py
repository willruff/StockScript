class Crypto:
    def __init__(self, name, price, supply):
        # crypto values
        self.name = name
        self.price = price
        self.supply = supply
        self.marketCap = price * supply

    # exact same as stock adjust_price, only different is supply instead of shares
    def adjust_price(self, adjustment):
        if adjustment.__class__.__name__ == 'PercentValue':
            percent = float(adjustment.value)
            percent_change = self.price * (percent / 100)
            self.price += percent_change
        elif adjustment.__class__.__name__ == 'NumericValue':
            change = float(adjustment.value)
            self.price += change
            
        self.marketCap = self.price * self.supply

    # exact same as stock merge, only different is supply instead of shares
    def merge(self, other_crypto):
        if not isinstance(other_crypto, Crypto):
            raise ValueError("Can only merge with another Crypto object.")
        
        total_supply = self.supply + other_crypto.supply
        weighted_price = (
            (self.price * self.supply + other_crypto.price * other_crypto.supply) / 
            total_supply
        )
        
        self.supply = total_supply
        self.price = weighted_price
        self.marketCap = self.price * self.supply
        
        return self

    # displat all crypto coins
    def display(self, display_type='all'):
        print(f"Crypto: {self.name}")
        if display_type in ['market_cap', 'all']:
            print(f"  Market Cap: ${self.marketCap:.0f}")
        if display_type in ['price', 'all']:
            print(f"  Price: ${self.price:.2f}")
        if display_type in ['supply', 'all']:
            print(f"  Supply: {self.supply:.0f}")