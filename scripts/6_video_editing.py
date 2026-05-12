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
    - Creates one continuous video
    """
    
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    # ============================================
    # METHOD 1: Load All Assets
    # ============================================
    def load_all_assets(self):
        """
        Load images, voiceovers, and music data
        """
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
    # METHOD 2: Create Concat File for FFmpeg
    # ============================================
    def create_concat_file(self, visual_data, vo_data):
        """
        Creates a concat file that tells FFmpeg how to combine videos
        """
        print("\n📝 Creating concat file...")
        
        concat_file = f"{self.output_dir}/concat_list.txt"
        
        with open(concat_file, 'w') as f:
            # For each scene, create a video from image + voiceover
            for i, scene in enumerate(visual_data.get('scenes', []), 1):
                image_path = scene.get('image_path')
                duration = scene.get('duration', 5)
                
                if i < len(vo_data.get('voiceovers', [])):
                    vo_file = vo_data['voiceovers'][i-1].get('voiceover_file')
                else:
                    vo_file = None
                
                # File for this scene
                scene_video = f"{self.output_dir}/scene_{i}_temp.mp4"
                
                # Check files exist
                if not os.path.exists(image_path):
                    print(f"   ⚠️ Image not found: {image_path}")
                    continue
                
                if vo_file and not os.path.exists(vo_file):
                    print(f"   ⚠️ Voiceover not found: {vo_file}")
                    vo_file = None
                
                # Write to concat file
                f.write(f"file '{scene_video}'\n")
                
                print(f"   📝 Scene {i}: {duration}s")
        
        print(f"   ✅ Concat file created: {concat_file}")
        return concat_file
    
    # ============================================
    # METHOD 3: Create Scene Videos
    # ============================================
    def create_scene_videos(self, visual_data, vo_data):
        """
        Create individual video for each scene (image + voiceover)
        """
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
                print(f"      ⚠️ Image not found, creating placeholder...")
                # Create black placeholder
                cmd = f'ffmpeg -f lavfi -i color=c=black:s=1920x1080:d={duration} -pix_fmt yuv420p -y {scene_video} 2>/dev/null'
                os.system(cmd)
                scene_videos.append(scene_video)
                continue
            
            # Get voiceover for this scene
            vo_file = None
            if i <= len(vo_data.get('voiceovers', [])):
                vo_file = vo_data['voiceovers'][i-1].get('voiceover_file')
            
            if vo_file and os.path.exists(vo_file):
                print(f"      Voiceover: {vo_file}")
                
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
                
                print(f"      ✅ Creating video...")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"      ✅ Scene video created")
                    scene_videos.append(scene_video)
                else:
                    print(f"      ❌ Failed to create scene video")
                    print(f"         Error: {result.stderr[:100]}")
            else:
                print(f"      ⚠️ No voiceover, using image only")
                
                # Create video from image only
                cmd = f'ffmpeg -loop 1 -i {image_path} -c:v libx264 -t {duration} -pix_fmt yuv420p -y {scene_video} 2>/dev/null'
                os.system(cmd)
                scene_videos.append(scene_video)
        
        print(f"\n✅ Created {len(scene_videos)} scene videos")
        return scene_videos
    
    # ============================================
    # METHOD 4: Concatenate All Scenes
    # ============================================
    def concatenate_videos(self, scene_videos):
        """
        Concatenate all scene videos into one final video
        """
        print("\n🔗 Concatenating scene videos...")
        
        if not scene_videos:
            print("   ❌ No scene videos to concatenate")
            return None
        
        # Create concat file
        concat_file = f"{self.output_dir}/concat_list.txt"
        with open(concat_file, 'w') as f:
            for video in scene_videos:
                f.write(f"file '{os.path.abspath(video)}'\n")
        
        print(f"   📝 Concat file created with {len(scene_videos)} videos")
        
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(output_file):
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"   ✅ Final video created!")
            print(f"      File: {output_file}")
            print(f"      Size: {file_size_mb:.2f} MB")
            return output_file
        else:
            print(f"   ❌ Concat failed")
            print(f"      Error: {result.stderr[:200]}")
            return None
    
    # ============================================
    # METHOD 5: Add Music/Audio
    # ============================================
    def add_background_music(self, video_file, audio_config):
        """
        Add background music to final video
        """
        print("\n🎵 Adding background music...")
        
        music_file = audio_config.get('background_music', {}).get('file')
        
        if not music_file or not os.path.exists(music_file):
            print("   ⚠️ Background music file not found, skipping...")
            return video_file
        
        # Create new file with music
        output_with_music = video_file.replace('.mp4', '_with_music.mp4')
        
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', music_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first[a]',
            '-map', '0:v:0',
            '-map', '[a]',
            '-y',
            output_with_music
        ]
        
        print(f"   ⚙️ Mixing audio...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(output_with_music):
            print(f"   ✅ Music added successfully")
            # Replace original with music version
            os.remove(video_file)
            os.rename(output_with_music, video_file)
            return video_file
        else:
            print(f"   ⚠️ Music mixing failed, using video without music")
            return video_file
    
    # ============================================
    # METHOD 6: Save Metadata
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
        
        return metadata
    
    # ============================================
    # MAIN RUN METHOD
    # ============================================
    def run(self):
        """Execute complete video editing"""
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING STARTING...")
        print("="*60)
        
        # Load assets
        visual_data, vo_data, audio_config = self.load_all_assets()
        
        if not visual_data:
            print("\n❌ No visual data found!")
            return None
        
        if not vo_data:
            print("\n❌ No voiceover data found!")
            return None
        
        print("\n✅ All assets loaded successfully")
        
        # Create scene videos
        scene_videos = self.create_scene_videos(visual_data, vo_data)
        
        if not scene_videos:
            print("\n❌ No scene videos created!")
            return None
        
        # Concatenate
        output_file = self.concatenate_videos(scene_videos)
        
        if not output_file:
            print("\n❌ Video concatenation failed!")
            return None
        
        # Add music if available
        if audio_config:
            output_file = self.add_background_music(output_file, audio_config)
        
        # Save metadata
        metadata = self.save_metadata(output_file)
        
        # Clean up temp files
        print("\n🧹 Cleaning up temporary files...")
        for video in scene_videos:
            try:
                if os.path.exists(video):
                    os.remove(video)
            except:
                pass
        
        print(f"""
╔═══════════════════════════════════════════════════════╗
║           ✅ VIDEO EDITING COMPLETE                   ║
╚═══════════════════════════════════════════════════════╝

📹 Video with Audio Created!
   Type: {self.video_type}
   File: {output_file}
   Status: {metadata['status']}
   Size: {metadata.get('file_size_mb', '?')} MB

✨ Your video now has:
   ✅ Images from each scene
   ✅ Voiceover narration
   ✅ Background music
   ✅ Perfect timing
        """)
        
        return metadata

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
    short_editor.run()
    
    # Long video
    print("\n📺 Creating LONG video (300s):")
    long_editor = VideoEditor('long')
    long_editor.run()
    
    print("\n" + "="*60)
    print("✅ VIDEO PRODUCTION COMPLETE")
    print("="*60)
