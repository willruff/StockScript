class Stock:
    def __init__(self, name, price, shares):
        # stock values
        self.name = name
        self.price = price
        self.shares = shares
        self.marketCap = price * shares

    # adjust price by percentage or dollar amount
    def adjust_price(self, adjustment):
        # check if input is a percentage
        if adjustment.__class__.__name__ == 'PercentValue':
            percent = float(adjustment.value)
            percent_change = self.price * (percent / 100)
            self.price += percent_change
        # else check if it is a numericValue (float)
        elif adjustment.__class__.__name__ == 'NumericValue':
            change = float(adjustment.value)
            self.price += change
            
        self.marketCap = self.price * self.shares

    # stock split operation
    def split(self, ratio):
        if hasattr(ratio, 'value'):
            ratio_value = float(ratio.value)
        else:
            ratio_value = float(ratio)
        # execute the split
        self.shares *= ratio_value
        self.price /= ratio_value
    
    # stock reverse split
    def rsplit(self, ratio):
        if hasattr(ratio, 'value'):
            ratio_value = float(ratio.value)
        else:
            ratio_value = float(ratio)
        # execute the reverse split
        self.shares /= ratio_value
        self.price *= ratio_value
    
    # stock merge (weighted)
    def merge(self, other_stock):
        if not isinstance(other_stock, Stock):
            raise ValueError("Can only merge with another Stock object.")

        # adds shares together
        total_shares = self.shares + other_stock.shares
        # equation to get the new weighted price per share
        weighted_price = (
            (self.price * self.shares + other_stock.price * other_stock.shares) / 
            total_shares
        )
        
        # update new merged stocks value
        self.shares = total_shares
        self.price = weighted_price
        self.marketCap = self.price * self.shares
        
        return self

    # display the stock values
    def display(self, display_type='all'):
        print(f"Stock: {self.name}")
        if display_type in ['market_cap', 'all']:
            print(f"  Market Cap: ${self.marketCap:.0f}")
        if display_type in ['price', 'all']:
            print(f"  Price: ${self.price:.2f}")
        if display_type in ['shares', 'all']:
            print(f"  Shares: {self.shares:.0f}")