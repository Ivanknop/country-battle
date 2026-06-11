import csv
import os
import random
from model.country import Country

script_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(script_path, "..", "files", "normalized_countries.csv")
_countries_cache = None
def _load_all():
    global _countries_cache
    if _countries_cache is None:
        _countries_cache = []
        with open(csv_path, "r", encoding="utf8") as f:
            for row in csv.DictReader(f):
                characteristics = {
                    "gdp_per_capita": float(row["gdp_per_capita"]),
                    "gdp_growth": float(row["gdp_growth"]),
                    "military_expenditure": float(row["military_expenditure"]),
                    "literacy_rate": float(row["literacy_rate"]),
                    "human_capital_index": float(row["human_capital_index"]),
                    "health_expenditure": float(row["health_expenditure"]),
                    "tertiary_enrollment": float(row["tertiary_enrollment"]),
                    "science_investment": float(row["science_investment"]),
                    "life_expectancy": float(row["life_expectancy"]),
                    "population": float(row["population"])
                }
                country = Country(row["name"], characteristics)
                _countries_cache.append(country)
    return _countries_cache

def load_countries():
    return _load_all()

def find_country(name):
    return next((c for c in _load_all() if c.get_name() == name), None)

def random_country_excluding(name):
    options = [c for c in _load_all() if c.get_name() != name]
    return random.choice(options)