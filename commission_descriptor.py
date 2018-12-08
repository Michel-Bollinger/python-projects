

class Value:
    """
    A descriptor class that subtracts a commission 
    when a value is assigned to an attribute. 
    Script for mastering the concept of descriptors, 
    no practical application.
    """
    def __init__(self):
        self.value = None

    def __get__(self, instance, instance_type):
        return self.value

    def __set__(self, instance, value):
        self.value = int((1 - instance.commission) * value)


class Amount:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission

account = Amount(0.1)
account.amount = 100
print(account.amount)
