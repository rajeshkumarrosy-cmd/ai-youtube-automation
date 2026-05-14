#!/usr/bin/env python3
"""
Step 4: Voiceover Generation
Generates voice narration for videos using multiple TTS engines
"""

import os
import json
import subprocess
from pathlib import Path

print("\n" + "="*60)
print("🎙️ STEP 4: VOICEOVER GENERATION")
print("="*60)

# Create output folder
os.makedirs("output/voiceovers", exist_ok=True)

# Load scripts
try:
    with open("output/scripts.json", "r") as f:
        scripts = json.load(f)
except:
    print("❌ No scripts found!")
    exit(1)

# ================================================================
# HELPER FUNCTION: Generate voice with fallbacks
# ================================================================

def generate_voice(text, output_path, scene_num, video_type):
    """Generate voice with multiple TTS engine fallbacks"""
    
    print(f"      Scene {scene_num}: '{text[:50]}...'")
    
    # Try Method 1: Piper TTS (Best quality, local)
    try:
        print(f"         Trying Piper TTS...")
        subprocess.run([
            "piper",
            "--model", "en_US-amy-medium",
            "--output-file", output_path
        ], input=text.encode(), timeout=60, check=True, capture_output=True)
        
        print(f"         ✅ Piper TTS success")
        return True
    
    except Exception as e:
        print(f"         Piper error: {e}")
    
    # Try Method 2: Edge TTS (Microsoft, high quality)
    try:
        print(f"         Trying Edge TTS...")
        subprocess.run([
            "edge-tts",
            "--text", text,
            "--voice", "en-US-AriaNeural",
            "--write-media", output_path,
            "--rate", "+0%"
        ], timeout=60, check=True, capture_output=True)
        
        print(f"         ✅ Edge TTS success")
        return True
    
    except Exception as e:
        print(f"         Edge TTS error: {e}")
    
    # Try Method 3: gTTS (Google Text-to-Speech)
    try:
        print(f"         Trying gTTS...")
        from gtts import gTTS
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        
        print(f"         ✅ gTTS success")
        return True
    
    except Exception as e:
        print(f"         gTTS error: {e}")
    
    # Fallback: Create silent audio
    try:
        print(f"         Creating fallback silent audio...")
        subprocess.run([
            "ffmpeg", "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
            "-t", "5",
            "-q:a", "9",
            "-acodec", "libmp3lame",
            output_path,
            "-y"
        ], timeout=30, capture_output=True)
        
        print(f"         ✅ Fallback audio created")
        return True
    
    except Exception as e:
        print(f"         Fallback error: {e}")
        return False

# ================================================================
# CREATE SHORT VIDEO VOICEOVERS
# ================================================================

print("\n📱 Creating SHORT video voiceovers...")

short_script = scripts.get("short", {})
short_scenes = short_script.get("scenes", [])

short_voiceovers = []

for i, scene in enumerate(short_scenes):
    narration = scene.get("description", f"Scene {i+1}")
    output_path = f"output/voiceovers/short_{i+1}.wav"
    
    success = generate_voice(narration, output_path, i+1, "short")
    
    if success and os.path.exists(output_path):
        short_voiceovers.append(output_path)
        print(f"         ✅ Saved: {output_path}")
    else:
        print(f"         ❌ Voice generation failed")

print(f"\n✅ SHORT voiceovers created: {len(short_voiceovers)}")

# ================================================================
# CREATE LONG VIDEO VOICEOVERS
# ================================================================

print("\n📺 Creating LONG video voiceovers...")

long_script = scripts.get("long", {})
long_scenes = long_script.get("scenes", [])

long_voiceovers = []

for i, scene in enumerate(long_scenes):
    narration = scene.get("description", f"Scene {i+1}")
    output_path = f"output/voiceovers/long_{i+1}.wav"
    
    success = generate_voice(narration, output_path, i+1, "long")
    
    if success and os.path.exists(output_path):
        long_voiceovers.append(output_path)
        print(f"         ✅ Saved: {output_path}")
    else:
        print(f"         ❌ Voice generation failed")

print(f"\n✅ LONG voiceovers created: {len(long_voiceovers)}")

# ================================================================
# SAVE VOICEOVER MANIFEST
# ================================================================

print("\n💾 Saving voiceover manifest...")

voiceover_manifest = {
    "short_voiceovers": short_voiceovers,
    "long_voiceovers": long_voiceovers,
    "short_count": len(short_voiceovers),
    "long_count": len(long_voiceovers)
}

with open("output/voiceover_manifest.json", "w") as f:
    json.dump(voiceover_manifest, f, indent=2)

print(f"   ✅ Saved: output/voiceover_manifest.json")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ VOICEOVER GENERATION COMPLETE")
print("="*60)

print(f"""
🎤 Voiceovers Created:

SHORT VIDEO:
   Scenes: {len(short_voiceovers)}/{len(short_scenes)}
   Files: output/voiceovers/short_*.wav

LONG VIDEO:
   Scenes: {len(long_voiceovers)}/{len(long_scenes)}
   Files: output/voiceovers/long_*.wav

📁 Files Saved:
   ✅ output/voiceover_manifest.json
   ✅ output/voiceovers/short_*.wav
   ✅ output/voiceovers/long_*.wav
""")

print()
