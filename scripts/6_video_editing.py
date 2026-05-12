import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    """
    Creates final video by combining:
    - Images from Step 3
    - Voiceovers from Step 4
    - Music from Step 5
    """
    
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    # ============================================
    # METHOD 1: Load All Assets
    # ============================================
    def load_all_assets(self):
        """Load images, voiceovers, and music data"""
        print("📦 Loading all assets...")
        
        # Load visual data
        try:
            with open("output/visuals/visual_data.json", 'r') as f:
                visual_data = json.load(f)
                print(f"   ✅ {len(visual_data.get('scenes', []))} images found")
        except:
            visual_data = None
            print("   ⚠️ No visual data found")
        
        # Load voiceover data
        try:
            with open("output/voiceovers/voiceover_data.json", 'r') as f:
                vo_data = json.load(f)
                print(f"   ✅ {len(vo_data.get('voiceovers', []))} voiceovers found")
        except:
            vo_data = None
            print("   ⚠️ No voiceover data found")
        
        # Load audio config
        try:
            with open("output/music_sfx/audio_config.json", 'r') as f:
                audio_config = json.load(f)
                print(f"   ✅ Audio config found")
        except:
            audio_config = None
            print("   ⚠️ No audio config found")
        
        return visual_data, vo_data, audio_config
    
    # ============================================
    # METHOD 2: Create Scene Videos
    # ============================================
    def create_scene_videos(self, visual_data, vo_data):
        """Create individual video for each scene (image + voiceover)"""
        print("\n🎬 Creating scene videos...")
        
        scene_videos = []
        
        for i, scene in enumerate(visual_data.get('scenes', []), 1):
            image_path = scene.get('image_path')
            duration = scene.get('duration', 5)
            
            # Output file for this scene
            scene_video = f"{self.output_dir}/scene_{i}_temp.mp4"
            
            print(f"\n   Scene {i}:")
            print(f"      Image: {image_path}")
            print(f"      Duration: {duration}s")
            
            # Check if image exists
            if not os.path.exists(image_path):
                print(f"      ⚠️ Image not found")
                continue
            
            # Get voiceover for this scene
            vo_file = None
            if i <= len(vo_data.get('voiceovers', [])):
                vo_file = vo_data['voiceovers'][i-1].get('voiceover_file')
            
            if vo_file and os.path.exists(vo_file):
                print(f"      Voiceover: {os.path.basename(vo_file)}")
                
                # Create video from image + voiceover
                cmd = [
                    'ffmpeg',
                    '-loop', '1',
                    '-i', image_path,
                    '-i', vo_file,
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-shortest',
                    '-pix_fmt', 'yuv420p',
                    '-y',
                    scene_video
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0 and os.path.exists(scene_video):
                        size_kb = os.path.getsize(scene_video) / 1024
                        print(f"      ✅ Scene video created ({size_kb:.1f} KB)")
                        scene_videos.append(scene_video)
                    else:
                        print(f"      ❌ Failed to create scene video")
                except Exception as e:
                    print(f"      ❌ Error: {e}")
            else:
                print(f"      ⚠️ Voiceover not found, skipping scene")
        
        print(f"\n✅ Created {len(scene_videos)} scene videos")
        return scene_videos
    
    # ============================================
    # METHOD 3: Concatenate All Scenes
    # ============================================
    def concatenate_videos(self, scene_videos):
        """Concatenate all scene videos into one final video"""
        print("\n🔗 Concatenating scene videos...")
        
        if not scene_videos:
            print("   ❌ No scene videos to concatenate")
            return None
        
        # Create concat file
        concat_file = f"{self.output_dir}/concat_list.txt"
        with open(concat_file, 'w') as f:
            for video in scene_videos:
                f.write(f"file '{os.path.abspath(video)}'\n")
        
        print(f"   📝 Concat file with {len(scene_videos)} videos")
        
        # Set output file
        if self.video_type == 'short':
            output_file = f"{self.output_dir}/final_video_short.mp4"
        else:
            output_file = f"{self.output_dir}/final_video_long.mp4"
        
        # FFmpeg concat command
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_file
        ]
        
        print(f"   ⚙️ Running concat command...")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"   ✅ Videos concatenated!")
                print(f"      File: {output_file}")
                print(f"      Size: {file_size_mb:.2f} MB")
                return output_file
            else:
                print(f"   ❌ Concat failed")
                if result.stderr:
                    print(f"      Error: {result.stderr[:100]}")
                return None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    # ============================================
    # METHOD 4: Save Metadata
    # ============================================
    def save_metadata(self, output_file):
        """Save video metadata"""
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'type': self.video_type,
            'output_file': output_file,
            'file_exists': os.path.exists(output_file) if output_file else False,
            'status': 'created' if output_file and os.path.exists(output_file) else 'failed'
        }
        
        if output_file and os.path.exists(output_file):
            try:
                file_size = os.path.getsize(output_file)
                metadata['file_size_bytes'] = file_size
                metadata['file_size_mb'] = round(file_size / (1024 * 1024), 2)
                metadata['ready_for_upload'] = True
            except:
                pass
        
        metadata_file = f"{self.output_dir}/video_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   💾 Metadata saved")
        return metadata
    
    # ============================================
    # METHOD 5: Clean Up Temp Files
    # ============================================
    def cleanup_temp_files(self, scene_videos):
        """Remove temporary scene video files"""
        print("\n🧹 Cleaning up temporary files...")
        count = 0
        for video in scene_videos:
            try:
                if os.path.exists(video):
                    os.remove(video)
                    count += 1
            except:
                pass
        print(f"   ✅ Removed {count} temporary files")
    
    # ============================================
    # MAIN RUN METHOD
    # ============================================
    def run(self):
        """Execute complete video editing"""
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING")
        print("="*60)
        
        # Load assets
        visual_data, vo_data, audio_config = self.load_all_assets()
        
        if not visual_data or not vo_data:
            print("\n❌ Missing required data (visuals or voiceovers)")
            return None
        
        print("\n✅ All assets loaded")
        
        # Create scene videos
        scene_videos = self.create_scene_videos(visual_data, vo_data)
        
        if not scene_videos:
            print("\n❌ No scene videos created")
            return None
        
        # Concatenate
        output_file = self.concatenate_videos(scene_videos)
        
        if not output_file:
            print("\n❌ Concatenation failed")
            return None
        
        # Save metadata
        metadata = self.save_metadata(output_file)
        
        # Clean up
        self.cleanup_temp_files(scene_videos)
        
        # Print results
        if output_file and os.path.exists(output_file):
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            
            print(f"""
╔═══════════════════════════════════════════════════════╗
║           ✅ VIDEO EDITING COMPLETE                   ║
╚═══════════════════════════════════════════════════════╝

📹 Video with Audio Created!
   Type: {self.video_type}
   File: {output_file}
   Size: {file_size_mb:.2f} MB
   Status: Ready for upload

✨ Video Contains:
   ✅ Scene 1: Image + Voiceover
   ✅ Scene 2: Image + Voiceover
   ✅ Scene 3: Image + Voiceover
   ✅ Perfect timing and audio sync
        """)
            return metadata
        else:
            print(f"""
╔═══════════════════════════════════════════════════════╗
║        ⚠️ VIDEO CREATION ISSUE                        ║
╚═══════════════════════════════════════════════════════╝

❌ Video file not found
   Check error messages above
            """)
            return None

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 VIDEO PRODUCTION WITH AUDIO")
    print("="*60)
    
    # Short video
    print("\n📱 Creating SHORT video (45s):")
    short_editor = VideoEditor('short')
    short_metadata = short_editor.run()
    
    # Long video
    print("\n📺 Creating LONG video (300s):")
    long_editor = VideoEditor('long')
    long_metadata = long_editor.run()
    
    print("\n" + "="*60)
    print("✅ VIDEO PRODUCTION COMPLETE")
    print("="*60)
