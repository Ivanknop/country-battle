from battle_core.entity import Entity

class Country(Entity):
    "creat a country"
    def __init__(self, name, characteristics):
        vitality = self.calculate_vitality(characteristics)
        super().__init__(name, vitality, characteristics)
        self.vitality = vitality
    
    def calculate_vitality(self, characteristics):
        return (characteristics["population"] + (characteristics["population"] * ( 
                characteristics["human_capital_index"] * 0.2 + 
                characteristics["health_expenditure"] * 0.1 + characteristics["life_expectancy"] * 0.5 )))
    
    def _vitality_modifier(self):
        vitality_ratio = self.vitality / self.initial_vitality
        damage_taken = 1 - vitality_ratio
        decay_steps = int(damage_taken / 0.1)
        return max(1 - (decay_steps * 0.05), 0.5)
    
    def offensive_power(self):
        base_power = self.characteristics["military_expenditure"] * 0.5 + self.characteristics["gdp_growth"] * 0.1 + self.characteristics["science_investment"] * 0.1 + self.characteristics["gdp_per_capita"] * 0.3
        return base_power * self._vitality_modifier()

    def defensive_power(self):
        base_defense =  self.characteristics["human_capital_index"] * 0.2 + self.characteristics["health_expenditure"] * 0.2 + self.characteristics["life_expectancy"] * 0.3
        return base_defense * self._vitality_modifier() 

    def initiative(self):
        base_initiative = self.characteristics["military_expenditure"] * 0.4 + self.characteristics["gdp_per_capita"] * 0.3 + self.characteristics["human_capital_index"] * 0.2 + self.characteristics["health_expenditure"] * 0.1
        return base_initiative * self._vitality_modifier()  
