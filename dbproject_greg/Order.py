class Order(object):
    def __init__(self, id, member, product, R_Date, D_Date, total, I_No):
        self.id = id
        self.member = member
        self.product =product
        self.R_Date = R_Date
        self.D_Date = D_Date
        self.total = total
        self.I_No = I_No