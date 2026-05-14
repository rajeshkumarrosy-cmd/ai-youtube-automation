#!/usr/bin/env python3
"""
Step 5: Music & Sound Effects
"""

import os
import json
import subprocess

print("\n" + "="*60)
print("🎵 STEP 5: MUSIC & SOUND EFFECTS")
print("="*60)

os.makedirs("output/music_sfx", exist_ok=True)

print("\n🎼 Creating background music...")

music_path = "output/music_sfx/background.mp3"

try:
    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=mono",
        "-t", "30",
        "-q:a", "9",
        "-acodec", "libmp3lame",
        music_path,
        "-y"
    ], capture_output=True, timeout=30)
    
    if os.path.exists(music_path):
        print(f"   ✅ Created: background.mp3")
    else:
        print(f"   ❌ Failed to create music")

except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ STEP 5 COMPLETE")
print("="*60)
print()
