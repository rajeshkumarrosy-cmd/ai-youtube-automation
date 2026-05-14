#!/usr/bin/env python3
"""
Step 6: Video Editing & Assembly
Combines images, voiceovers, and music into final videos
"""

import os
import json
from moviepy.editor import *

print("\n" + "="*60)
print("🎬 STEP 6: VIDEO EDITING & ASSEMBLY")
print("="*60)

# Create videos folder
os.makedirs("output/videos", exist_ok=True)

# Load manifests
try:
    with open("output/visuals_manifest.json", "r") as f:
        visuals = json.load(f)
    with open("output/voiceover_manifest.json", "r") as f:
        voiceovers = json.load(f)
except Exception as e:
    print(f"❌ Missing manifest files: {e}")
    exit(1)

# ================================================================
# CREATE SHORT VIDEO
# ================================================================

print("\n📱 Creating SHORT video...")

short_visuals = visuals.get("short_visuals", [])
short_voices = voiceovers.get("short_voiceovers", [])

if len(short_visuals) > 0 and len(short_voices) > 0:
    try:
        # Load voiceover to get duration
        narration = AudioFileClip(short_voices[0])
        duration = narration.duration
        
        # Create image clips
        clips = []
        for visual in short_visuals:
            if os.path.exists(visual):
                clip = ImageClip(visual).set_duration(duration / len(short_visuals))
                clip = clip.resize(height=1920)
                clips.append(clip)
        
        if clips:
            # Combine
            video = concatenate_videoclips(clips)
            
            # Add audio
            if len(short_voices) > 0:
                audio = AudioFileClip(short_voices[0])
                video = video.set_audio(audio)
            
            # Add caption
            caption = TextClip("Subscribe!", fontsize=80, color='white', 
                             font='Arial-Bold', stroke_width=2, stroke_color='black')
            caption = caption.set_duration(duration).set_position(('center', 'bottom'))
            video = CompositeVideoClip([video, caption])
            
            # Save
            output = "output/videos/final_short.mp4"
            print(f"   ⏳ Rendering... (this takes 2-5 minutes)")
            video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac',
                                verbose=False, logger=None)
            print(f"   ✅ Created: {output}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ❌ Missing visuals or voices")

# ================================================================
# CREATE LONG VIDEO
# ================================================================

print("\n📺 Creating LONG video...")

long_visuals = visuals.get("long_visuals", [])
long_voices = voiceovers.get("long_voiceovers", [])

if len(long_visuals) > 0 and len(long_voices) > 0:
    try:
        # Load voiceover
        narration = AudioFileClip(long_voices[0])
        duration = narration.duration
        
        # Create image clips
        clips = []
        for visual in long_visuals:
            if os.path.exists(visual):
                clip = ImageClip(visual).set_duration(duration / len(long_visuals))
                clip = clip.resize(height=1080)
                clips.append(clip)
        
        if clips:
            # Combine
            video = concatenate_videoclips(clips)
            
            # Add audio
            if len(long_voices) > 0:
                audio = AudioFileClip(long_voices[0])
                video = video.set_audio(audio)
            
            # Add caption
            caption = TextClip("Subscribe!", fontsize=80, color='white',
                             font='Arial-Bold', stroke_width=2, stroke_color='black')
            caption = caption.set_duration(duration).set_position(('center', 'bottom'))
            video = CompositeVideoClip([video, caption])
            
            # Save
            output = "output/videos/final_long.mp4"
            print(f"   ⏳ Rendering... (this takes 5-10 minutes)")
            video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac',
                                verbose=False, logger=None)
            print(f"   ✅ Created: {output}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ❌ Missing visuals or voices")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ VIDEO EDITING COMPLETE")
print("="*60)
print()
