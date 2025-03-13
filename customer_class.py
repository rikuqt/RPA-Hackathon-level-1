from dataclasses import dataclass, astuple

@dataclass
class Customer():
    Product_Name: str
    Quantity: str
    Price: str
    Customer_Name: str
    Customer_Address: str
    Customer_Email: str
    Delivery_Date: str

    def __iter__(self):
        return iter(astuple(self))