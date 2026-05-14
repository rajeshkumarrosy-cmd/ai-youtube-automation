#!/usr/bin/env python3
"""
Step 6: Video Editing
Combines images + voiceovers + music into final videos
"""

import os
import json
from moviepy.editor import *

print("\n" + "="*60)
print("🎬 STEP 6: VIDEO EDITING")
print("="*60)

# Load visuals manifest
try:
    with open("output/visuals_manifest.json", "r") as f:
        visuals = json.load(f)
except:
    print("❌ No visuals found!")
    exit(1)

# Create videos folder
os.makedirs("output/videos", exist_ok=True)

# ================================================================
# CREATE SHORT VIDEO
# ================================================================

print("\n📱 Creating SHORT video...")

short_visuals = visuals.get("short_visuals", [])
short_voiceovers = [f for f in os.listdir("output/voiceovers") if f.startswith("short_")]

if len(short_visuals) == 0:
    print("   ❌ No short visuals found!")
else:
    print(f"   Loading {len(short_visuals)} images...")
    
    try:
        # Get duration from first voiceover
        if short_voiceovers:
            first_vo = AudioFileClip(f"output/voiceovers/{short_voiceovers[0]}")
            total_duration = first_vo.duration
        else:
            total_duration = 30
        
        print(f"   Total duration: {total_duration:.1f} seconds")
        
        # Create image clips
        clips = []
        image_duration = total_duration / len(short_visuals)
        
        for visual_path in short_visuals:
            if os.path.exists(visual_path):
                clip = ImageClip(visual_path).set_duration(image_duration)
                clip = clip.resize(height=1920)  # Vertical format
                clips.append(clip)
        
        if clips:
            # Combine clips
            video = concatenate_videoclips(clips)
            
            # Add voiceover
            if short_voiceovers:
                vo_files = [f"output/voiceovers/{f}" for f in short_voiceovers if os.path.exists(f"output/voiceovers/{f}")]
                if vo_files:
                    voiceovers = [AudioFileClip(f) for f in vo_files]
                    narration = concatenate_audioclips(voiceovers)
                    
                    # Add music if available
                    music_files = [f for f in os.listdir("output/music_sfx") if f.endswith((".mp3", ".wav"))]
                    if music_files:
                        music_path = f"output/music_sfx/{music_files[0]}"
                        try:
                            music = AudioFileClip(music_path).volumex(0.2).set_duration(total_duration)
                            final_audio = CompositeAudioClip([narration, music])
                        except:
                            final_audio = narration
                    else:
                        final_audio = narration
                    
                    video = video.set_audio(final_audio)
            
            # Add caption
            caption = TextClip(
                "Subscribe!",
                fontsize=80,
                color='white',
                font='Arial-Bold',
                stroke_width=2,
                stroke_color='black'
            ).set_duration(total_duration).set_position(('center', 'bottom'))
            
            video = CompositeVideoClip([video, caption])
            
            # Render
            short_output = "output/videos/final_short.mp4"
            print(f"   ⏳ Rendering short video (2-5 minutes)...")
            
            video.write_videofile(
                short_output,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"   ✅ Short video created: {short_output}")
    
    except Exception as e:
        print(f"   ❌ Error creating short video: {e}")

# ================================================================
# CREATE LONG VIDEO
# ================================================================

print("\n📺 Creating LONG video...")

long_visuals = visuals.get("long_visuals", [])
long_voiceovers = [f for f in os.listdir("output/voiceovers") if f.startswith("long_")]

if len(long_visuals) == 0:
    print("   ❌ No long visuals found!")
else:
    print(f"   Loading {len(long_visuals)} images...")
    
    try:
        # Get duration from first voiceover
        if long_voiceovers:
            first_vo = AudioFileClip(f"output/voiceovers/{long_voiceovers[0]}")
            total_duration = first_vo.duration
        else:
            total_duration = 60
        
        print(f"   Total duration: {total_duration:.1f} seconds")
        
        # Create image clips
        clips = []
        image_duration = total_duration / len(long_visuals)
        
        for visual_path in long_visuals:
            if os.path.exists(visual_path):
                clip = ImageClip(visual_path).set_duration(image_duration)
                clip = clip.resize(height=1080)  # Horizontal format
                clips.append(clip)
        
        if clips:
            # Combine clips
            video = concatenate_videoclips(clips)
            
            # Add voiceover
            if long_voiceovers:
                vo_files = [f"output/voiceovers/{f}" for f in long_voiceovers if os.path.exists(f"output/voiceovers/{f}")]
                if vo_files:
                    voiceovers = [AudioFileClip(f) for f in vo_files]
                    narration = concatenate_audioclips(voiceovers)
                    
                    # Add music if available
                    music_files = [f for f in os.listdir("output/music_sfx") if f.endswith((".mp3", ".wav"))]
                    if music_files:
                        music_path = f"output/music_sfx/{music_files[0]}"
                        try:
                            music = AudioFileClip(music_path).volumex(0.2).set_duration(total_duration)
                            final_audio = CompositeAudioClip([narration, music])
                        except:
                            final_audio = narration
                    else:
                        final_audio = narration
                    
                    video = video.set_audio(final_audio)
            
            # Add caption
            caption = TextClip(
                "Subscribe!",
                fontsize=80,
                color='white',
                font='Arial-Bold',
                stroke_width=2,
                stroke_color='black'
            ).set_duration(total_duration).set_position(('center', 'bottom'))
            
            video = CompositeVideoClip([video, caption])
            
            # Render
            long_output = "output/videos/final_long.mp4"
            print(f"   ⏳ Rendering long video (5-10 minutes)...")
            
            video.write_videofile(
                long_output,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"   ✅ Long video created: {long_output}")
    
    except Exception as e:
        print(f"   ❌ Error creating long video: {e}")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ VIDEO EDITING COMPLETE")
print("="*60)

print(f"""
📹 Output Videos:
   📱 Short: output/videos/final_short.mp4
   📺 Long:  output/videos/final_long.mp4

✨ Features:
   ✅ Colorful scene backgrounds
   ✅ Human-like voice narration
   ✅ Background music
   ✅ Professional captions
   ✅ Ready for YouTube!
""")
