#!/usr/bin/env python3
"""
Step 6: Video Editing & Assembly
"""

import os
import json
from moviepy.editor import *

print("\n" + "="*60)
print("🎬 STEP 6: VIDEO EDITING & ASSEMBLY")
print("="*60)

os.makedirs("output/videos", exist_ok=True)

# Load data
try:
    with open("output/visuals_manifest.json", "r") as f:
        visuals = json.load(f)
    with open("output/voiceover_manifest.json", "r") as f:
        voiceovers = json.load(f)
except Exception as e:
    print(f"❌ Error loading manifests: {e}")
    exit(1)

# ================================================================
# CREATE SHORT VIDEO
# ================================================================

print("\n📱 Creating SHORT video...")

short_visuals = [f for f in visuals.get("short_visuals", []) if os.path.exists(f)]
short_voices = [f for f in voiceovers.get("short_voiceovers", []) if os.path.exists(f)]

if len(short_visuals) > 0:
    try:
        print(f"   Images: {len(short_visuals)}")
        print(f"   Voices: {len(short_voices)}")
        
        # Get duration
        try:
            narration = AudioFileClip(short_voices[0]) if short_voices else None
            duration = narration.duration if narration else 10
        except:
            duration = 10
        
        # Create clips
        clips = []
        for visual in short_visuals:
            try:
                clip = ImageClip(visual).set_duration(duration / len(short_visuals))
                clip = clip.resize(height=1920)
                clips.append(clip)
            except:
                pass
        
        if clips:
            print(f"   ⏳ Assembling video...")
            video = concatenate_videoclips(clips)
            
            # Add audio if available
            if short_voices:
                try:
                    audio = AudioFileClip(short_voices[0])
                    video = video.set_audio(audio)
                except:
                    pass
            
            # Add caption
            try:
                caption = TextClip("Subscribe!", fontsize=80, color='white',
                                 font='Arial-Bold', stroke_width=2, stroke_color='black')
                caption = caption.set_duration(duration).set_position(('center', 'bottom'))
                video = CompositeVideoClip([video, caption])
            except:
                pass
            
            # Render
            output = "output/videos/final_short.mp4"
            print(f"   ⏳ Rendering... (2-5 minutes)")
            
            try:
                video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac',
                                    verbose=False, logger=None)
                print(f"   ✅ Created: final_short.mp4")
            except Exception as e:
                print(f"   ❌ Render error: {str(e)[:100]}")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
else:
    print(f"   ⚠️ No images found")

# ================================================================
# CREATE LONG VIDEO
# ================================================================

print("\n📺 Creating LONG video...")

long_visuals = [f for f in visuals.get("long_visuals", []) if os.path.exists(f)]
long_voices = [f for f in voiceovers.get("long_voiceovers", []) if os.path.exists(f)]

if len(long_visuals) > 0:
    try:
        print(f"   Images: {len(long_visuals)}")
        print(f"   Voices: {len(long_voices)}")
        
        # Get duration
        try:
            narration = AudioFileClip(long_voices[0]) if long_voices else None
            duration = narration.duration if narration else 30
        except:
            duration = 30
        
        # Create clips
        clips = []
        for visual in long_visuals:
            try:
                clip = ImageClip(visual).set_duration(duration / len(long_visuals))
                clip = clip.resize(height=1080)
                clips.append(clip)
            except:
                pass
        
        if clips:
            print(f"   ⏳ Assembling video...")
            video = concatenate_videoclips(clips)
            
            # Add audio if available
            if long_voices:
                try:
                    audio = AudioFileClip(long_voices[0])
                    video = video.set_audio(audio)
                except:
                    pass
            
            # Add caption
            try:
                caption = TextClip("Subscribe!", fontsize=80, color='white',
                                 font='Arial-Bold', stroke_width=2, stroke_color='black')
                caption = caption.set_duration(duration).set_position(('center', 'bottom'))
                video = CompositeVideoClip([video, caption])
            except:
                pass
            
            # Render
            output = "output/videos/final_long.mp4"
            print(f"   ⏳ Rendering... (5-10 minutes)")
            
            try:
                video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac',
                                    verbose=False, logger=None)
                print(f"   ✅ Created: final_long.mp4")
            except Exception as e:
                print(f"   ❌ Render error: {str(e)[:100]}")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
else:
    print(f"   ⚠️ No images found")

print("\n" + "="*60)
print("✅ STEP 6 COMPLETE")
print("="*60)
print()
