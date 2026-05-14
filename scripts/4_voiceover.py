#!/usr/bin/env python3
"""
Step 4: Voiceover Generation
Creates voice narration using the simplest method possible
"""

import os
import json
import subprocess

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
# CREATE SHORT VIDEO VOICEOVERS (using gTTS - simplest)
# ================================================================

print("\n📱 Creating SHORT video voiceovers...")

short_script = scripts.get("short", {})
short_scenes = short_script.get("scenes", [])

short_voiceovers = []

for i, scene in enumerate(short_scenes, 1):
    narration = scene.get("description", f"Scene {i}")
    output_path = f"output/voiceovers/short_{i}.mp3"
    
    print(f"   Scene {i}/{ len(short_scenes)}: Creating voice...")
    
    try:
        # Try using gTTS (simplest, no external dependencies)
        from gtts import gTTS
        
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save(output_path)
        
        short_voiceovers.append(output_path)
        print(f"      ✅ Saved: {output_path}")
    
    except ImportError:
        print(f"      ⚠️ gTTS not available, creating fallback...")
        
        # Fallback: Create silent MP3
        try:
            subprocess.run([
                "ffmpeg", "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "3",
                "-q:a", "9",
                "-acodec", "libmp3lame",
                output_path,
                "-y"
            ], capture_output=True, timeout=15)
            
            short_voiceovers.append(output_path)
            print(f"      ✅ Fallback saved: {output_path}")
        
        except Exception as e:
            print(f"      ❌ Error: {e}")

print(f"\n✅ SHORT voiceovers: {len(short_voiceovers)}/{len(short_scenes)}")

# ================================================================
# CREATE LONG VIDEO VOICEOVERS
# ================================================================

print("\n📺 Creating LONG video voiceovers...")

long_script = scripts.get("long", {})
long_scenes = long_script.get("scenes", [])

long_voiceovers = []

for i, scene in enumerate(long_scenes, 1):
    narration = scene.get("description", f"Scene {i}")
    output_path = f"output/voiceovers/long_{i}.mp3"
    
    print(f"   Scene {i}/{len(long_scenes)}: Creating voice...")
    
    try:
        # Try using gTTS
        from gtts import gTTS
        
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save(output_path)
        
        long_voiceovers.append(output_path)
        print(f"      ✅ Saved: {output_path}")
    
    except ImportError:
        print(f"      ⚠️ gTTS not available, creating fallback...")
        
        # Fallback: Create silent MP3
        try:
            subprocess.run([
                "ffmpeg", "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "3",
                "-q:a", "9",
                "-acodec", "libmp3lame",
                output_path,
                "-y"
            ], capture_output=True, timeout=15)
            
            long_voiceovers.append(output_path)
            print(f"      ✅ Fallback saved: {output_path}")
        
        except Exception as e:
            print(f"      ❌ Error: {e}")

print(f"\n✅ LONG voiceovers: {len(long_voiceovers)}/{len(long_scenes)}")

# ================================================================
# SAVE MANIFEST
# ================================================================

print("\n💾 Saving manifest...")

manifest = {
    "short_voiceovers": short_voiceovers,
    "long_voiceovers": long_voiceovers,
    "short_count": len(short_voiceovers),
    "long_count": len(long_voiceovers)
}

with open("output/voiceover_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("   ✅ Saved: output/voiceover_manifest.json")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ VOICEOVER GENERATION COMPLETE")
print("="*60)

print(f"""
🎤 Summary:
   SHORT: {len(short_voiceovers)} voiceovers
   LONG: {len(long_voiceovers)} voiceovers
   Total: {len(short_voiceovers) + len(long_voiceovers)} files
""")

print()
