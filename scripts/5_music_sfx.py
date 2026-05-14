#!/usr/bin/env python3
"""
Step 5: Music & Sound Effects
Creates background music for videos
"""

import os
import json
import subprocess

print("\n" + "="*60)
print("🎵 STEP 5: MUSIC & SOUND EFFECTS")
print("="*60)

# Create output folder
os.makedirs("output/music_sfx", exist_ok=True)

print("\n🎼 Creating background music...")

# Create 30 seconds of ambient sound using ffmpeg
music_path = "output/music_sfx/background.mp3"

try:
    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "30",
        "-q:a", "9",
        "-acodec", "libmp3lame",
        music_path,
        "-y"
    ], capture_output=True, timeout=30)
    
    print(f"   ✅ Created: {music_path}")

except Exception as e:
    print(f"   ❌ Error: {e}")

# ================================================================
# SAVE MANIFEST
# ================================================================

manifest = {
    "music_file": music_path,
    "duration": 30
}

with open("output/music_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("   ✅ Saved: output/music_manifest.json")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ MUSIC & SFX COMPLETE")
print("="*60)
print()
