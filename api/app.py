import traceback
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from model.country_fight import CountryFight
import model.handler_csv as handler_csv 
from model.country_combat_rules import CountryCombatRules
from model.country import Country
import random

def country_to_session(country):
    return {
        "name": country.get_name(),
        "vitality": country.get_vitality(),
        "initial_vitality": country.initial_vitality,
        "characteristics": country.get_characteristics()
    }

def country_from_session(data):
    country = Country(data["name"], data["characteristics"])
    country.vitality = data["vitality"]
    country.initial_vitality = data["initial_vitality"]
    return country


def create_app():
    app = Flask(__name__)
    app.secret_key ="country-secret"
    @app.route('/')
    def index():
        return render_template('index.html')

    # Ruta que se ingresa por la ULR 127.0.0.1:5000
    @app.route("/countries")
    def countries():
        try:
            data = handler_csv.load_countries()
            return render_template('table.html', data=data)
        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500       

    @app.route("/choose_country")
    def choose_country():
        try:
            data = handler_csv.load_countries()
            return render_template("choose_country.html", country_db=data)

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/start_fight", methods=["GET"])
    def start_fight():
        try:
            name_country = request.args.get("jugador")
            a_country = handler_csv.find_country(name_country)
            opponent = handler_csv.random_country_excluding(name_country)
            session["fighter_one"] = country_to_session(a_country)
            session["fighter_two"] = country_to_session(opponent)
            session["events"] = []
            session["finished"] = False
            session["winner"] = None
            session["winner_role"] = None
            session["attacker_luck"] = 0
            session["defender_luck"] = 0
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
            session["luck_used_this_turn"] = False
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/fight", methods=["GET"])
    def fight_screen():
        try:
            fighter_one = session.get("fighter_one")
            fighter_two = session.get("fighter_two")
            events = session.get("events", [])
            finished = session.get("finished", False)
            winner = session.get("winner")
            winner_role = session.get("winner_role")

            if fighter_one is None or fighter_two is None:
                return redirect(url_for("choose_country"))
            return render_template(
                "fight.html",
                fighter_one=fighter_one,
                fighter_two=fighter_two,
                events=events,
                finished=finished,
                winner=winner,
                winner_role=winner_role,
                attacker_luck=session.get("attacker_luck", 0),
                defender_luck=session.get("defender_luck", 0),
                pending_attacker_luck=session.get("pending_attacker_luck"),
                pending_defender_luck=session.get("pending_defender_luck"),
                luck_used_this_turn=session.get("luck_used_this_turn", False),
            )

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/fight/next", methods=["POST"])
    def next_turn():
        try:
            fighter_one_data = session.get("fighter_one")
            fighter_two_data = session.get("fighter_two")
            if fighter_one_data is None or fighter_two_data is None:
                return redirect(url_for("choose_country"))
            fighter_one = country_from_session(fighter_one_data)
            fighter_two = country_from_session(fighter_two_data)
            battle = CountryFight(fighter_one, fighter_two)
            attacker_luck = int(session.get("attacker_luck", 0))
            defender_luck = int(session.get("defender_luck", 0))
            result = battle.play_turn(
                attacker_luck=attacker_luck,
                defender_luck=defender_luck,
            )
            session["fighter_one"] = country_to_session(fighter_one)
            session["fighter_two"] = country_to_session(fighter_two)
            events = session.get("events", [])
            for event in reversed(result):
                events.insert(0, event)
            session["events"] = events
            winner = battle.winner()
            if winner is not None:
                session["finished"] = True
                session["winner"] = winner.get_name()
                if winner.get_name() == fighter_one.get_name():
                    session["winner_role"] = "Jugador"
                else:
                    session["winner_role"] = "Rival"
            session["attacker_luck"] = 0
            session["defender_luck"] = 0
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
            session["luck_used_this_turn"] = False

            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
        
    @app.route("/fight/luck", methods=["POST"])
    def roll_luck():
        try:
            combat_rules = CountryCombatRules()
            luck_pair = combat_rules.roll_luck_pair(random)

            session["pending_attacker_luck"] = luck_pair["attacker_luck"]
            session["pending_defender_luck"] = luck_pair["defender_luck"]
            session["luck_used_this_turn"] = True
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    @app.route("/fight/luck/reject", methods=["POST"])
    def reject_luck():
        try:
            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None
            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500
    @app.route("/fight/luck/accept", methods=["POST"])
    def accept_luck():
        try:
            session["attacker_luck"] = session.get("pending_attacker_luck", 0)
            session["defender_luck"] = session.get("pending_defender_luck", 0)

            session["pending_attacker_luck"] = None
            session["pending_defender_luck"] = None

            return redirect(url_for("fight_screen"))

        except Exception:
            return jsonify({"trace": traceback.format_exc()}), 500

    return app
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)