def test_fighter():
    
    from model.country_fight import CountryFight
    from model.country import Country
    usa_characteristics = {
        "population": 10,
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
    usa = Country('USA', usa_characteristics)

    arg_characteristics = {
        "population": 10000000,
        "gdp_per_capita": 1,
        "gdp_growth": 1,
        "military_expenditure": 1,
        "literacy_rate": 1,
        "human_capital_index": 1,
        "health_expenditure": 1,
        "tertiary_enrollment": 1,
        "science_investment": 1,
        "life_expectancy": 1
    }
    arg = Country('ARG', arg_characteristics)
    round = CountryFight(usa, arg)
    assert round.get_fighter_one().get_name() == 'USA'
    assert round.get_fighter_two().get_name() == 'ARG'
    print(f"ARG offensive_power: {arg.offensive_power()}")
    print(f"USA defensive_power: {usa.defensive_power()}")
    print(f"USA vitality: {usa.get_vitality()}")
    events = round.play_turn(player_luck=0, opponent_luck=0)
    assert len(events) == 2
    assert usa.is_alive() is True
    round.play_turn(player_luck=0, opponent_luck=0)
    round.play_turn(player_luck=0, opponent_luck=0)
    assert round.winner().get_name() == "ARG"
