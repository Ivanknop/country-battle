from battle_core.entity import Entity

class Country(Entity):
    "creat a country"
    def __init__(self, name, characteristics):
        vitality = self.calculate_vitality(characteristics)
        super().__init__(name, vitality, characteristics)
    
    def calculate_vitality(self, characteristics):
        return (characteristics["population"] + (characteristics["population"] * ( 
                characteristics["human_capital_index"] * 0.2 + 
                characteristics["health_expenditure"] * 0.1 + characteristics["life_expectancy"] * 0.5 )))

    def offensive_power(self):
        return self.characteristics["military_expenditure"] * 0.5 + self.characteristics["gdp_growth"] * 0.1 + self.characteristics["science_investment"] * 0.1 + self.characteristics["gdp_per_capita"] * 0.3

    def defensive_power(self):
        return (self.characteristics["military_expenditure"] * 0.4 +
            self.characteristics["gdp_per_capita"] * 0.25 +
            self.characteristics["human_capital_index"] * 0.2 +
            self.characteristics["health_expenditure"] * 0.15)

    def initiative(self):
        return self.characteristics["gdp_growth"] * 0.5 + self.characteristics["literacy_rate"] * 0.2 + self.characteristics["science_investment"] * 0.3
       
    def get_resistance(self):
        return self.get_vitality()
