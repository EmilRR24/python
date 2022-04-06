# ##four pillars

# ## TODO benifits 

# # keeping our code DRY


# ## TODO encapsulation


class CoffeeMachine:

    def __init__(self, filter_type, type = "coffee machine"):
        self.type = type
        self.filter_type = filter_type
        self.water_temp = 200

    def brew_coffee(self, beans = 'coffee beans'):
        print("coffee is ready")

    def clean(self):
        print("Someone left the wet filter in the machine over the weekend!!!")
        print("this is totally gross!!")

# ## TODO inheritance ## TODO polymorphism

class FrenchPress(CoffeeMachine):
    pass
    


class KCup(CoffeeMachine):

    def __init__(self, brand, type="coffee machine"):
        super().__init__(type) # this brings the attributes from the parent class that we want our child class to inherit.
        self.brand = brand

    def clean(self):
        print("throw the pod away")

class CappuccinoM( CoffeeMachine ):
    def __init__(self,name):
        super().__init__(name)
        self.milk = "whole"

    def make_cappuccino(self,beans):
        super.brew_coffee(beans)
        print("Frothy!!!")

    def clean(self):
        print("Cleaning the froth!")

# ## TODO abstraction

# mrcoffee = CoffeeMachine()
# fpress = FrenchPress()
