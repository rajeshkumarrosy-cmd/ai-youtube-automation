import os
import json

def check_all_files():
    print("\n" + "="*70)
    print("🔍 VIDEO GENERATION DIAGNOSTIC")
    print("="*70 + "\n")
    
    # Check Step 1
    print("✓ STEP 1: Trends")
    if os.path.exists("output/scripts/trending_topics.json"):
        print("   ✅ Trends file exists")
        try:
            with open("output/scripts/trending_topics.json") as f:
                data = json.load(f)
                topic = data.get('selected_topic', {}).get('title', 'Unknown')
                print(f"   📝 Topic: {topic}")
        except Exception as e:
            print(f"   ⚠️ Error reading file: {e}")
    else:
        print("   ❌ Trends file NOT found")
    
    # Check Step 2
    print("\n✓ STEP 2: Scripts")
    if os.path.exists("output/scripts/short_script.json"):
        print("   ✅ Short script exists")
        try:
            with open("output/scripts/short_script.json") as f:
                data = json.load(f)
                scenes = len(data.get('scenes', []))
                print(f"   📝 Scenes: {scenes}")
        except Exception as e:
            print(f"   ⚠️ Error reading file: {e}")
    else:
        print("   ❌ Short script NOT found")
    
    if os.path.exists("output/scripts/long_script.json"):
        print("   ✅ Long script exists")
    else:
        print("   ❌ Long script NOT found")
    
    # Check Step 3
    print("\n✓ STEP 3: Visuals")
    if os.path.exists("output/visuals/visual_data.json"):
        print("   ✅ Visual data exists")
        try:
            with open("output/visuals/visual_data.json") as f:
                data = json.load(f)
                total = len(data.get('scenes', []))
                print(f"   🎬 Video clips: {total}")
                
                for scene in data.get('scenes', []):
                    video_file = scene.get('file')
                    if os.path.exists(video_file):
                        size = os.path.getsize(video_file) / (1024 * 1024)
                        print(f"      ✅ Scene {scene['scene']}: {size:.2f} MB")
                    else:
                        print(f"      ❌ Scene {scene['scene']}: FILE NOT FOUND - {video_file}")
        except Exception as e:
            print(f"   ⚠️ Error reading file: {e}")
    else:
        print("   ❌ Visual data NOT found")
        print("   ❌ Checking for scene files...")
        for i in range(1, 5):
            if os.path.exists(f"output/visuals/scene_{i}.mp4"):
                size = os.path.getsize(f"output/visuals/scene_{i}.mp4") / (1024 * 1024)
                print(f"      ✅ Scene {i}: {size:.2f} MB")
    
    # Check Step 4
    print("\n✓ STEP 4: Voiceovers")
    if os.path.exists("output/voiceovers/voiceover_data.json"):
        print("   ✅ Voiceover data exists")
        try:
            with open("output/voiceovers/voiceover_data.json") as f:
                data = json.load(f)
                total = len(data.get('voiceovers', []))
                print(f"   🎤 Voiceovers: {total}")
                
                for vo in data.get('voiceovers', []):
                    audio_file = vo.get('file')
                    if os.path.exists(audio_file):
                        size = os.path.getsize(audio_file) / 1024
                        print(f"      ✅ Scene {vo['scene']}: {size:.1f} KB")
                    else:
                        print(f"      ❌ Scene {vo['scene']}: FILE NOT FOUND - {audio_file}")
        except Exception as e:
            print(f"   ⚠️ Error reading file: {e}")
    else:
        print("   ❌ Voiceover data NOT found")
        print("   ❌ Checking for audio files...")
        for i in range(1, 5):
            if os.path.exists(f"output/voiceovers/scene_{i}.mp3"):
                size = os.path.getsize(f"output/voiceovers/scene_{i}.mp3") / 1024
                print(f"      ✅ Scene {i}: {size:.1f} KB")
    
    # Check Step 6
    print("\n✓ STEP 6: Final Video")
    if os.path.exists("output/videos/final_video_short.mp4"):
        print("   ✅ FINAL VIDEO EXISTS!")
        try:
            size = os.path.getsize("output/videos/final_video_short.mp4") / (1024 * 1024)
            print(f"   📹 Size: {size:.2f} MB")
            print(f"   📍 Path: output/videos/final_video_short.mp4")
        except Exception as e:
            print(f"   ⚠️ Error getting size: {e}")
    else:
        print("   ❌ FINAL VIDEO NOT FOUND!")
        
        print("\n   Checking for scene_X_final.mp4 files...")
        for i in range(1, 5):
            scene_file = f"output/videos/scene_{i}_final.mp4"
            if os.path.exists(scene_file):
                try:
                    size = os.path.getsize(scene_file) / (1024 * 1024)
                    print(f"      ✅ Scene {i}: {size:.2f} MB")
                except:
                    print(f"      ✅ Scene {i}: EXISTS (can't read size)")
            else:
                print(f"      ❌ Scene {i}: NOT FOUND")
    
    # Summary
    print("\n" + "="*70)
    print("🔍 DIAGNOSTIC COMPLETE")
    print("="*70)
    
    # Check if main video exists
    if os.path.exists("output/videos/final_video_short.mp4"):
        print("\n✅ SUCCESS! Video file created!")
        print("📹 Download: output/videos/final_video_short.mp4")
    else:
        print("\n❌ VIDEO NOT CREATED")
        print("⚠️ Check which step failed above")
    
    print("\n")

if __name__ == "__main__":
    check_all_files()
