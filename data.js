// Aggregator — data.js is now assembled from the split files below.
// Load order in index.html: data/topics/*.js, data/deep-dives.js,
// data/resources.js, then this file. Regenerate with:
//   python extract\tools\split_data_js.py
const topics = [].concat(
  _t_intro_behavior,
  _t_behavioral_psych,
  _t_social_psych,
  _t_body_language,
  _t_cognitive_biases,
  _t_personality,
  _t_nonverbal_codes,
  _t_deception_detection,
  _t_emotion_expression,
  _t_impression_mgmt,
  _t_interpersonal_dynamics,
  _t_reading_people,
  _t_moral_psychology,
  _t_evolutionary_psych,
  _t_biological_bases,
  _t_attachment_relationships,
  _t_existential_humanistic,
  _t_body_language_extracted,
)
const deepDives = _deepDives
const resources = _resources
