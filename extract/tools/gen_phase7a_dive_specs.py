# -*- coding: utf-8 -*-
"""Generate authoring specs for the Phase 7A deep dives (2 per book, 16 total)."""
import io
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7a", "dives")
os.makedirs(OUT, exist_ok=True)

COMMON = {
    "job": "deep_dive",
    "output_dir": os.path.abspath(OUT),
    "schema": {
        "title": "string, plain English title",
        "framework_description": "intro paragraph, then exactly 3 marked sections separated by \\n: \"\\n.1. Heading Here\\n...paragraph...\", \"\\n.2. ...\", \"\\n.3. ...\"",
        "key_takeaways": "array of exactly 4 English takeaways",
        "sections": "array of exactly 2 objects: { heading: str, source: str (format 'AuthorName, Initial. (Year)'), body: str (2-3 sentences) }",
        "svg": "single-line SVG string: only <rect> and <text> elements; viewBox=\"0 0 820 300\"; first element is <rect width=\"820\" height=\"300\" fill=\"#181825\" rx=\"10\" for the dark background; ends with </svg>",
        "sv": {
            "title": "natural Swedish title",
            "framework_description": "Swedish version with the same .\\n.1/.2/.3 structure",
            "key_takeaways": "exactly 4 Swedish takeaways",
            "sections": "exactly 2 objects: { heading, body } in Swedish, no source field"
        }
    },
    "quality_bar": [
        "psychologically accurate and measured; only claims the book actually makes; both languages natural, correct, zero typos",
        "no markdown, no backticks; no [] or {} characters inside any string value",
        "exactly the fields above and nothing more"
    ]
}

DIVES = [
    # Kahneman -> cognitive-biases
    {
        "spec_file": "kahneman_dive1.json", "dive_topic_key": "cognitive-biases",
        "content": "The two-systems model of Kahneman (System 1 fast/intuitive/automatic, System 2 slow/deliberate/effortful): how each performs, when System 1 leads us astray (the lazy System 2, WYSIATI - what you see is all there is), cognitive ease and the expert-intuition debate (recognition-based skill vs overconfident intuition quoting Meehl and the conditions for valid intuition), and everyday consequences (first impressions, marketing, risk perception).",
    },
    {
        "spec_file": "kahneman_dive2.json", "dive_topic_key": "cognitive-biases",
        "content": "Heuristics and the biases they produce: representativeness (base-rate neglect, conjunction fallacy with Linda), availability (fluent examples inflate probability, dread risk, risk-perception gap), anchoring and adjustment (adjustment is insufficient; real-world anchors in pricing and negotiation), and what to do about them (consider the opposite, slowing down, external validity check).",
    },
    # Power of Habit -> choice-architecture
    {
        "spec_file": "poh_dive1.json", "dive_topic_key": "choice-architecture",
        "content": "The habit loop as popularized by Duhigg: cue, routine, reward, and the craving that drives it; how habits are stored in the basal ganglia, why they persist without conscious memory; keystone habits (small changes that cascade: exercise, making your bed); the two-minute rule and golden rule of habit change (keep the cue and the reward, change the routine).",
    },
    {
        "spec_file": "poh_dive2.json", "dive_topic_key": "choice-architecture",
        "content": "Organizational and societal habit change from Duhigg's reporting: how companies engineer habits (Febreze, Target's pregnancy prediction), the role of willpower as a learnable habit, belief and community in recovery (AA, the importance of a believing group at turning points), and the limits - what popular habit advice simplifies about the underlying science.",
    },
    # Mindset -> personality
    {
        "spec_file": "mindset_dive1.json", "dive_topic_key": "personality",
        "content": "Fixed vs growth mindset as defined by Dweck: beliefs about the malleability of intelligence and ability, how each mindset reacts to challenge, effort, and failure; praise experiments (praising effort vs intelligence in children and its effects on later persistence); the danger of 'growth mindset' as a buzzword (false growth mindset, all-or-nothing self-labeling).",
    },
    {
        "spec_file": "mindset_dive2.json", "dive_topic_key": "personality",
        "content": "Applying mindset research to real life from Dweck: mindset in school and parenting (fostering challenging tasks), in sports (Caster Semenya and attitude narratives), in business (talent myth vs organizational learning culture), and in relationships; the mechanics of changing mindset over time and what the replication debate does and does not undermine.",
    },
    # Lucifer Effect -> social-psych
    {
        "spec_file": "lucifer_dive1.json", "dive_topic_key": "social-psych",
        "content": "The Stanford Prison Experiment as documented by Zimbardo: design, the nine days, the forces at work (deindividuation through uniforms and roles, anonymity, diffusion of responsibility, dehumanization, the banality of evil and situational attribution); the criticisms and debates about the SPE's validity (selection effects, demand characteristics, the BBC prison study), and Milgram's obedience experiments as the companion evidence.",
    },
    {
        "spec_file": "lucifer_dive2.json", "dive_topic_key": "social-psych",
        "content": "The Lucifer Effect framework for resisting evil: the graduated steps of character erosion (small compromises, foot-in-the-door), the Abu Ghraib case as the modern illustration, dispositional vs situational attribution errors, and Zimbardo's ten-step program for resistance (watch for small steps, question authority, resist groupthink, maintain personal identity).",
    },
    # Emotional Intelligence -> interpersonal-dynamics
    {
        "spec_file": "ei_dive1.json", "dive_topic_key": "interpersonal-dynamics",
        "content": "The amygdala hijack from Goleman: how the emotional brain routes signals faster than the neocortex (thalamus-amygdala shortcut), what a hijack looks like in daily life (loss of working memory, preemptive reactions), and the role of the 'emotional concierge' in decision making (somatic markers, Damasio); how EQ research measures emotional self-regulation (Mayer-Salovey model vs Goleman's popular framing and the measurement debates).",
    },
    {
        "spec_file": "ei_dive2.json", "dive_topic_key": "interpersonal-dynamics",
        "content": "Empathy and social intelligence from Goleman: the three kinds (cognitive, emotional, empathic concern), emotional contagion and mirror systems, why empathy matters for relationships and leadership, the empathic-management and listening skills promoted in the book, and what research does and doesn't support about empathy training improving real-world outcomes.",
    },
    # Drive -> personality
    {
        "spec_file": "drive_dive1.json", "dive_topic_key": "personality",
        "content": "Self-determination theory as popularized by Pink: intrinsic vs extrinsic motivation, autonomy/mastery/purpose as innate needs, the overjustification effect and the candle problem (behavioral research showing extrinsic rewards narrow focus), and the practical redesign of tasks, workplaces (Results-Only Work Environment), and education toward autonomy.",
    },
    {
        "spec_file": "drive_dive2.json", "dive_topic_key": "personality",
        "content": "Motivation 1.0/2.0/3.0 and the application layer of Drive: the mismatch between carrot-and-stick management and complex creative work (sapient vs algorithmic tasks), Type I vs Type X behavior, flow and its conditions, failed/backfired incentive programs from Pink's case studies, and the limits of the popular framing relative to the underlying Deci & Ryan research.",
    },
    # Gift of Fear -> reading-people
    {
        "spec_file": "gof_dive1.json", "dive_topic_key": "reading-people",
        "content": "Intuition and pre-incident indicators (PINs) from de Becker: the gift of fear as an ancient warning system, why intuition is a fast, pattern-based 'computer that no one programmed', denial as the main obstacle (I don't want to believe it'), how PINs accumulate into a recognizable escalation pattern, and the difference between worry (unfocused) and fear (focused signal).",
    },
    {
        "spec_file": "gof_dive2.json", "dive_topic_key": "reading-people",
        "content": "Reading and defusing threatening behavior from de Becker: the interview techniques he teaches (open-ended questions, letting the subject talk, detecting deception through detail and relevance rather than body-language tells; the 'tyranny of relative safety' and the value of being unreasonable under threat), plus the limits of his case-based method versus controlled research.",
    },
    # Dark Psychology -> dark-triad
    {
        "spec_file": "dp_dive1.json", "dive_topic_key": "dark-triad",
        "content": "The dark psychology taxonomy presented in the compilation: the dark triad traits (narcissism, Machiavellianism, psychopathy), covert manipulation channels (love bombing, gaslighting, triangulation, smear campaigns, guilt-tripping), and the persuasion levers the book catalogs (mirroring, reciprocity, authority, scarcity, social proof). Frame defensively: these tactics are described to recognize and resist them, not to perpetrate them.",
    },
    {
        "spec_file": "dp_dive2.json", "dive_topic_key": "dark-triad",
        "content": "Defense and boundary-setting against manipulative influence from the compilation: recognizing manipulation patterns (test requests, sudden intimacy, victim narratives, isolation moves), protecting boundaries (broken-record responses, time-outs, documentation, exit strategies), and the popular-claim caveat: the book is an unscientific taxonomy and detection advice must be treated cautiously, not as validated profiling.",
    },
]

for d in DIVES:
    s = dict(COMMON)
    s.update(d)
    with io.open(os.path.join(OUT, d["spec_file"]), "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)
    print("wrote spec", d["spec_file"])