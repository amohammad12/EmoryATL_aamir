#!/usr/bin/env python3
"""Test Bark TTS installation"""

import torch
from transformers import AutoProcessor, BarkModel

print("🎵 Testing Bark TTS Installation...")
print(f"✓ PyTorch version: {torch.__version__}")
print(f"✓ CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    try:
        print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
    except Exception:
        print("✓ GPU available (name could not be retrieved)")

print("\n📥 Loading Bark model (this will download ~2-3GB on first run)...")
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained(
    "suno/bark",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

if torch.cuda.is_available():
    model = model.to("cuda")
    print("✓ Model loaded on GPU")
else:
    print("⚠ Model loaded on CPU (will be slower)")

print("\n🎤 Generating test audio...")
inputs = processor("♪ Yo-ho-ho and a bottle of rum! ♪", voice_preset="v2/en_speaker_6")

if torch.cuda.is_available():
    inputs = {k: v.to("cuda") for k, v in inputs.items()}

with torch.no_grad():
    audio = model.generate(**inputs)

print("✅ Success! Bark is working correctly.")
print("\nYou can now run the full application.")

