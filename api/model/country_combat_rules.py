from battle_core.combat_rules import CombatRules

class CountryCombatRules(CombatRules):
    def calculate_base_damage(self, attacker, defender):
        raw_damage = attacker.offensive_power() - defender.defensive_power()
        return max(1, raw_damage * defender.get_initial_vitality() * 0.3)