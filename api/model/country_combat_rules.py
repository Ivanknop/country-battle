from unittest import result

from battle_core.combat_rules import CombatRules

class CountryCombatRules(CombatRules):
    def calculate_base_damage(self, attacker, defender):
        offense = attacker.offensive_power()
        defense_reduction = min(defender.defensive_power() * 0.5, 0.7)  # máx 70% reducción
        raw_damage = offense * (1 - defense_reduction)
        return max(1, raw_damage * defender.initial_vitality * 0.5)