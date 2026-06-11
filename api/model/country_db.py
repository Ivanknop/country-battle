import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

model_path = os.path.dirname(os.path.realpath(__file__))
api_path = os.path.dirname(model_path)
database_path = os.path.join(api_path, "files", "countries.db")


class CountryDB(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    population = db.Column(db.Float, nullable=False)
    human_capital_index = db.Column(db.Float, nullable=False)
    health_expenditure = db.Column(db.Float, nullable=False)
    life_expectancy = db.Column(db.Float, nullable=False)
    military_expenditure = db.Column(db.Float, nullable=False)
    gdp_growth = db.Column(db.Float, nullable=False)
    science_investment = db.Column(db.Float, nullable=False)
    gdp_per_capita = db.Column(db.Float, nullable=False)
    literacy_rate = db.Column(db.Float, nullable=False)

    def get_name(self):
        return self.name

    def get_population(self):
        return self.population

    def get_human_capital_index(self):
        return self.human_capital_index

    def get_health_expenditure(self):
        return self.health_expenditure

    def get_life_expectancy(self):
        return self.life_expectancy

    def get_military_expenditure(self):
        return self.military_expenditure

    def get_gdp_growth(self):
        return self.gdp_growth

    def get_science_investment(self):
        return self.science_investment

    def get_gdp_per_capita(self):
        return self.gdp_per_capita

    def get_literacy_rate(self):
        return self.literacy_rate

    def get_speed(self):
        return self.speed
    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "human_capital_index": self.human_capital_index,
            "health_expenditure": self.health_expenditure,
            "life_expectancy": self.life_expectancy,
            "military_expenditure": self.military_expenditure,
            "gdp_growth": self.gdp_growth,
            "science_investment": self.science_investment,
            "gdp_per_capita": self.gdp_per_capita,
            "literacy_rate": self.literacy_rate
        }

    def __repr__(self):
        return f"<Country {self.name}>"