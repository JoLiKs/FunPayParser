class Flat:
    def __init__(self, link, reference=None, price=None, title=None, description=None, date=None):
        self.link = link
        self.reference = reference
        self.price = price
        self.title = title
        self.description = description
        self.date = date


class Lot:
    def __init__(self, link, reference=None, price=None, title=None, seller_rep=None):
        self.link = link
        self.reference = reference
        self.price = price
        self.title = title
        self.seller_rep = seller_rep
