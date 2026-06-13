def test_country_has_expected_characteristics():
    from model.country import Country

    country_characteristics = {
        "population": 1000000,
        "gdp_per_capita": 0.3,
        "gdp_growth": 0.2,
        "military_expenditure": 0.3,
        "literacy_rate": 0.05,
        "human_capital_index": 0.09,
        "health_expenditure": 0.25,
        "tertiary_enrollment": 0.1,
        "science_investment": 0.2,
        "life_expectancy": 0.5
    }
    usa = Country('USA', country_characteristics)

    assert usa.get_name() == "USA"
    assert usa.get_characteristics()["population"] == 1000000
    assert usa.get_characteristics()["gdp_per_capita"] == 0.3
    assert usa.get_characteristics()["gdp_growth"] == 0.2
    assert usa.get_characteristics()["military_expenditure"] == 0.3
    assert usa.get_characteristics()["literacy_rate"] == 0.05
    assert usa.get_characteristics()["human_capital_index"] == 0.09
    assert usa.get_characteristics()["health_expenditure"] == 0.25
    assert usa.get_characteristics()["tertiary_enrollment"] == 0.1
    assert usa.get_characteristics()["science_investment"] == 0.2
    assert usa.get_characteristics()["life_expectancy"] == 0.5

    assert usa.offensive_power() == 0.28
    assert usa.defensive_power() == 0.218
    assert usa.initiative() == 0.253
    assert usa.get_vitality() == 1293000.0
    