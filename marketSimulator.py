import random

class MarketSimulator:
    @staticmethod
    def get_random_change(sentiment, is_crypto=False):
        if sentiment == 'good_day':
            # good days: 1% to 7% for stocks, 5% to 15% for crypto
            base_range = (5, 15) if is_crypto else (1, 7)
            return random.uniform(base_range[0], base_range[1])
        elif sentiment == 'bad_day':
            # bad days: -7% to -1% for stocks, -15% to -5% for crypto
            base_range = (-15, -5) if is_crypto else (-7, -1)
            return random.uniform(base_range[0], base_range[1])
        else:
            # random days: -5% to 5% for stocks, -10% to 10% for crypto
            base_range = (-10, 10) if is_crypto else (-5, 5)
            return random.uniform(base_range[0], base_range[1])

    @staticmethod
    def apply_individual_variation(base_change):
        # Add some individual variation: ±2%
        return base_change + random.uniform(-2, 2)