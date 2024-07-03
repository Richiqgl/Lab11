
from dataclasses import dataclass
@dataclass
class Conteggio():
    Product_number1:int
    Product_number2: int
    Conteggio:int

    def __hash__(self):
        return hash(self.Product_number1+self.Product_number2)

    def __str__(self):
        return f" {self.Product_number1} - {self.Product_number2} - {self.Conteggio}"