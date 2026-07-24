import io, os, sys, wave
from piper import PiperVoice

_voices = {}
_models_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'tts-models'))

_LANG_MAP = {
    'en-US': 'en_US-lessac-medium',
    'sv-SE': 'sv_SE-alma-medium',
}

def _get_voice(lang):
    if lang in _voices:
        return _voices[lang]
    model = _LANG_MAP.get(lang, 'en_US-lessac-medium')
    model_path = os.path.join(_models_dir, model + '.onnx')
    config_path = model_path + '.json'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f'TTS model not found: {model_path}')
    _voices[lang] = PiperVoice.load(model_path, config_path=config_path)
    return _voices[lang]

def synthesize(text, lang='en-US'):
    voice = _get_voice(lang)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav:
        voice.synthesize_wav(text, wav)
    return buf.getvalue()

def preload_all():
    for lang in _LANG_MAP:
        try:
            _get_voice(lang)
            print(f'Loaded {lang} voice', file=sys.stderr)
        except Exception as e:
            print(f'Failed to load {lang} voice: {e}', file=sys.stderr)
