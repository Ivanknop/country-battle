from battle_core.fight import Fight
from model.country_combat_rules import CountryCombatRules
import random

class CountryFight(Fight):
    def __init__(self, fighter_one, fighter_two, rng=None):
        super().__init__(fighter_one, fighter_two, CountryCombatRules(), rng)

    def turn_text(self, attacker, defender, damage, attacker_luck, defender_luck, defender_initial_vitality):
        attacker_name = attacker.get_name()
        defender_name = defender.get_name()

        if self.get_combat_rules().is_automatic_failure(attacker_luck):
            frases = [
                f"{attacker_name} intentó una ofensiva pero fue neutralizada antes de comenzar.",
                f"La operación de {attacker_name} fracasó estrepitosamente.",
                f"{attacker_name} sufrió un revés diplomático y perdió la iniciativa.",
            ]
            return random.choice(frases)

        if self.get_combat_rules().is_blocked(attacker, defender, attacker_luck, defender_luck):
            frases = [
                f"{defender_name} interceptó la ofensiva de {attacker_name} causando solo {damage:.2f} de impacto.",
                f"Las defensas de {defender_name} absorbieron el ataque de {attacker_name}. Daño mínimo: {damage:.2f}.",
                f"{attacker_name} fue contenido por {defender_name} con pérdidas mínimas de {damage:.2f}.",
            ]
            return random.choice(frases)

        if self.get_combat_rules().critical_multiplier(attacker, defender, attacker_luck, defender_luck) > 1:
            frases = [
                f"¡{attacker_name} lanza un bombardeo masivo devastando a {defender_name} por {damage:.2f}!",
                f"¡Ataque relámpago de {attacker_name}! {defender_name} es saqueado por {damage:.2f}.",
                f"¡{attacker_name} desencadena una ofensiva total aplastando a {defender_name} con {damage:.2f} de daño!",
            ]
            return random.choice(frases)

        if defender_initial_vitality <= 0:
            return f"{attacker_name} remata a {defender_name} con un golpe final de {damage:.2f}."

        damage_ratio = damage / defender_initial_vitality

        if damage_ratio > 0.5:
            frases = [
                f"{attacker_name} bombardea {defender_name} causando {damage:.2f} de daño devastador.",
                f"Ofensiva brutal de {attacker_name} — {defender_name} pierde {damage:.2f} de resistencia.",
                f"{attacker_name} saquea las reservas de {defender_name} infligiendo {damage:.2f}.",
            ]
            return random.choice(frases)

        if damage_ratio < 0.1:
            frases = [
                f"{attacker_name} lanza una escaramuza menor contra {defender_name}. Impacto: {damage:.2f}.",
                f"Presión diplomática de {attacker_name} sobre {defender_name}. Daño simbólico: {damage:.2f}.",
                f"{attacker_name} impone sanciones leves a {defender_name} con efecto de {damage:.2f}.",
            ]
            return random.choice(frases)

        frases = [
            f"{attacker_name} intercepta rutas comerciales de {defender_name} causando {damage:.2f} de daño.",
            f"Operación encubierta de {attacker_name} debilita a {defender_name} en {damage:.2f}.",
            f"{attacker_name} presiona económicamente a {defender_name} con un impacto de {damage:.2f}.",
        ]
        return random.choice(frases)