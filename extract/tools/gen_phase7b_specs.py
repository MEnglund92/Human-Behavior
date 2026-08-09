# -*- coding: utf-8 -*-
r"""Generate per-batch authoring specs for Phase 7B topics 19 and 20.
Run: python extract\tools\gen_phase7b_specs.py
"""
import io
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7b")

FORBIDDEN = [
    "Behavior", "Stimulus", "Response", "Nature vs Nurture", "Empiricism", "Hypothesis",
    "Independent Variable", "Dependent Variable", "Correlation", "Operational Definition",
    "Structuralism", "Functionalism", "Behaviorism", "Cognitive Revolution",
    "Naturalistic Observation", "Positive Reinforcement", "Negative Reinforcement",
    "Punishment", "Extinction", "Habituation", "Cognitive Dissonance", "Loss Aversion",
    "Anchoring", "Availability", "Sunk Cost Fallacy", "Framing", "Halo Effect",
    "Confirmation Bias", "Conformity", "Obedience", "Self-Fulfilling Prophecy",
    "Heuristic", "Attribution", "Groupthink", "Bystander Effect", "Dark Triad",
    "Narcissism", "Machiavellianism", "Psychopathy", "Gaslighting",
]

T19 = [
    ("Choice Architecture", "choice-architecture", "Valarkitektur"),
    ("Default Option", "choice-architecture", "Standardalternativ"),
    ("Nudge", "choice-architecture", "Knuff"),
    ("Libertarian Paternalism", "choice-architecture", "Libertarisk paternalism"),
    ("Salience", "choice-architecture", "Saliens"),
    ("Choice Overload", "choice-architecture", "Valöverbelastning"),
    ("Status Quo Bias", "choice-architecture", "Status quo-bias"),
    ("Decoy Effect", "choice-architecture", "Lockbeteffekt"),
    ("Habit Loop", "habit-loops", "Vaneloop"),
    ("Habit Cue", "habit-loops", "Vanesignal"),
    ("Craving", "habit-loops", "Begär"),
    ("Habit Routine", "habit-loops", "Vanerutin"),
    ("Habit Reward", "habit-loops", "Vanebelöning"),
    ("Habit Stacking", "habit-loops", "Vanekedjning"),
    ("Temptation Bundling", "habit-loops", "Frestelsekoppling"),
    ("Implementation Intention", "habit-loops", "Implementeringsintention"),
    ("Identity-Based Habits", "habit-loops", "Identitetsbaserade vanor"),
    ("Goldilocks Rule", "habit-loops", "Guldlockregeln"),
    ("Friction", "friction-design", "Friktion"),
    ("Friction Reduction", "friction-design", "Friktionsreduktion"),
    ("Two-Minute Rule", "friction-design", "Tvåminutersregeln"),
    ("Environment Design", "friction-design", "Miljödesign"),
    ("Commitment Device", "friction-design", "Åtagandeinstrument"),
    ("Variable Reward", "friction-design", "Varierande belöning"),
]

T20 = [
    ("Gaslighting", "manipulation-tactics", "Gasbelysning"),
    ("Love Bombing", "toxic-dynamics", "Kärleksbombning"),
    ("Hoovering", "toxic-dynamics", "Återkontaktande"),
    ("Triangulation", "manipulation-tactics", "Triangulering"),
    ("Boundary Testing", "manipulation-tactics", "Gränstestande"),
    ("Emotional Blackmail", "manipulation-tactics", "Känslomässig utpressning"),
    ("Silent Treatment", "manipulation-tactics", "Tystnadsterapi"),
    ("Coercive Intermittent Reinforcement", "manipulation-tactics", "Tvångsartad intermittent förstärkning"),
    ("Trauma Bonding", "toxic-dynamics", "Traumabindning"),
    ("DARVO", "manipulation-tactics", "DARVO"),
    ("Flying Monkeys", "toxic-dynamics", "Medhjälpare"),
    ("Guilt Tripping", "manipulation-tactics", "Skuldbeläggning"),
    ("Covert Aggression", "manipulation-tactics", "Dold aggression"),
    ("Vulnerable Narcissism", "toxic-dynamics", "Sårbar narcissism"),
    ("Grey Rock Method", "defenses", "Grå klippa-metoden"),
    ("JADE Principle", "defenses", "JADE-principen"),
    ("Information Diet", "defenses", "Informationsdiet"),
]

CATS19 = {
    "choice-architecture": "Choice Architecture",
    "habit-loops": "Habit Loops",
    "friction-design": "Friction & Design",
}
CATS20 = {
    "manipulation-tactics": "Manipulation Tactics",
    "toxic-dynamics": "Toxic Dynamics",
    "defenses": "Defenses & Recovery",
}


def build_spec(topic_id, topic_name, cats, concepts):
    return {
        "topic_id": topic_id,
        "topic_name": topic_name,
        "categories": [{"id": k, "name": v} for k, v in cats.items()],
        "forbidden_concept_names": FORBIDDEN,
        "schema": {
            "concept": "string; must be the exact label from the entries list below",
            "definition": "one factual sentence, 12-25 words, plain language",
            "category": "string; one of the category ids",
            "real_world_scenario": "1-2 sentences (15-35 words), concrete real-life example",
            "case_study_cloze": "one sentence, exactly one blank written ____ (4 underscores); the concept label is the answer",
            "related_concepts": "array of exactly 2 strings (existing well-known psychology terms)",
            "sv": {
                "concept": "the Swedish label given below",
                "definition": "natural Swedish translation of the definition",
                "real_world_scenario": "Swedish version of the scenario, natural Swedish",
                "case_study_cloze": "Swedish sentence with one blank ____"
            }
        },
        "quality_bar": [
            "both languages correct, plain and idiomatic; zero typos; no invented or repeated words",
            "the cloze blank answer must equal the concept label word for word",
            "each entry exactly the fields above, nothing more",
            "write the file as valid JSON (UTF-8), no markdown, no code fences",
        ],
        "self_check": [
            "after writing the file run: python -c \"import json;print(len(json.load(open('FILE'))))\"",
            "report the entry count and the JSON-parse result in your final message",
        ],
        "entries": [{"concept": c[0], "category": c[1], "swedish_concept": c[2]} for c in concepts],
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    specs = [
        ("t19_b1.json", build_spec("choice-architecture", "19. Choice Architecture & Habit Mechanics", CATS19, T19[:8])),
        ("t19_b2.json", build_spec("choice-architecture", "19. Choice Architecture & Habit Mechanics", CATS19, T19[8:16])),
        ("t19_b3.json", build_spec("choice-architecture", "19. Choice Architecture & Habit Mechanics", CATS19, T19[16:])),
        ("t20.json", build_spec("dark-triad", "20. Dark Triad & Covert Manipulation", CATS20, T20)),
    ]
    for name, spec in specs:
        with io.open(os.path.join(OUT, "spec_" + name), "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False, indent=1)
        print("wrote spec_%s with %d entries" % (name, len(spec["entries"])))


if __name__ == "__main__":
    main()