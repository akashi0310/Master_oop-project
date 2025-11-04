class Promotion:
    def __init__(self, promo_id, code, discount_percent, min_purchase, valid_until, category):
        self.promo_id = promo_id
        self.code = code
        self.discount_percent = discount_percent
        self.min_purchase = min_purchase
        self.valid_until = valid_until
        self.category = category
        self.used_count = 0
