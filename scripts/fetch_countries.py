import requests
import csv

INDICATORS = {
    "population": "SP.POP.TOTL",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",
    "military_expenditure": "MS.MIL.XPND.GD.ZS",
    "literacy_rate": "SE.ADT.LITR.ZS",
    "human_capital_index": "HD.HCI.OVRL",
    "health_expenditure": "SH.XPD.CHEX.GD.ZS",
    "tertiary_enrollment": "SE.TER.ENRR",
    "science_investment": "GB.XPD.RSDV.GD.ZS",
    "male_population_pct": "SP.POP.TOTL.MA.ZS",
    "life_expectancy": "SP.DYN.LE00.IN",}

def is_real_country(country):
    return country['region']['id'] != 'NA'

def fetch_valid_iso3():
    url = "https://api.worldbank.org/v2/country"
    params = {"format": "json", "per_page": 300}
    response = requests.get(url, params=params)
    countries = response.json()[1]
    return {c['id'] for c in countries if is_real_country(c)}

def fetch_indicator(indicator_code, valid_iso3):
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}"
    params = {"format": "json", "per_page": 300, "mrv": 5}
    
    all_records = []
    page = 1
    total_pages = 1
    
    while page <= total_pages:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        total_pages = data[0]["pages"]
        all_records.extend(data[1])
        page += 1
    
    # quedarse con el dato más reciente no-nulo por país
    best = {}
    for record in all_records:
        iso3 = record["countryiso3code"]
        if iso3 not in valid_iso3:
            continue
        if record["value"] is None:
            continue
        if iso3 not in best:
            best[iso3] = record
        # mrv=5 devuelve de más reciente a más antiguo — el primero válido ya es el mejor
    
    return list(best.values())

def build_countries():
    valid_iso3 = fetch_valid_iso3()
    countries = {}  # diccionario, no lista
    
    for indicator_name, indicator_code in INDICATORS.items():
        records = fetch_indicator(indicator_code, valid_iso3)
        print(f"{indicator_name}: {len(records)} records")
        for record in records:
            iso3 = record['countryiso3code']
            if iso3 not in countries:
                countries[iso3] = {
                    'name': record['country']['value'],
                    **{key: None for key in INDICATORS.keys()}
                }
            countries[iso3][indicator_name] = record['value']
    
    return countries

def save_csv(countries, filename):
    output_path = f"../api/files/{filename}"
    fieldnames = ["iso3", "name", "population", "gdp_per_capita", "gdp_growth", 
                  "military_expenditure", "literacy_rate", "human_capital_index", "health_expenditure", "tertiary_enrollment", "science_investment", "male_population_pct", "life_expectancy"]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for iso3, data in countries.items():
            writer.writerow({
                "iso3": iso3,
                **data
            })


def normalize(countries):
    indicators_to_normalize = [
        "gdp_per_capita",
        "gdp_growth", 
        "military_expenditure",
        "literacy_rate",
        "human_capital_index",
        "health_expenditure",
        "tertiary_enrollment",
        "science_investment",
        "life_expectancy"
    ]
    
    for indicator in indicators_to_normalize:
        values = [c[indicator] for c in countries.values() if c[indicator] is not None]
        
        # 2. calcular min y max
        min_val = min(values)
        max_val = max(values)
        
        # 3. normalizar cada país
        for country in countries.values():
            if country[indicator] is not None:
                country[indicator] = (country[indicator] - min_val) / (max_val - min_val) if max_val != min_val else 0
            else:
                country[indicator] = 0  
                    
    return countries

if __name__ == "__main__":
    countries = build_countries()
    save_csv(countries,'country.csv')
    normalize_countries = normalize (countries)
    save_csv(normalize_countries,'normalized_countries.csv')
