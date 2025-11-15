change to Bark (Suno) — text → expressive audio (speech + simple musicality)
Transformer-based text→audio that can produce highly expressive speech and short musical/singing-like outputs; great for experiments where you want expressive, human-like prosody without heavy dataset work.

Installation
‼️ CAUTION ‼️ Do NOT use pip install bark. It installs a different package, which is not managed by Suno.

pip install git+https://github.com/suno-ai/bark.git
or

git clone https://github.com/suno-ai/bark
cd bark && pip install . 
🤗 Transformers Usage
Bark is available in the 🤗 Transformers library from version 4.31.0 onwards, requiring minimal dependencies and additional packages. Steps to get started:

First install the 🤗 Transformers library from main:
pip install git+https://github.com/huggingface/transformers.git
Run the following Python code to generate speech samples:
from transformers import AutoProcessor, BarkModel

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")

voice_preset = "v2/en_speaker_6"

inputs = processor("Hello, my dog is cute", voice_preset=voice_preset)

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()
Listen to the audio samples either in an ipynb notebook:
from IPython.display import Audio

sample_rate = model.generation_config.sample_rate
Audio(audio_array, rate=sample_rate)
Or save them as a .wav file using a third-party library, e.g. scipy:

import scipy

sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array)
For more details on using the Bark model for inference using the 🤗 Transformers library, refer to the Bark docs or the hands-on Google Colab.


I want it to work with project and integrate with other tools. use music mode in this.

