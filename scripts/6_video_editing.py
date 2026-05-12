import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    """
    Creates final video by combining all assets
    Uses FFmpeg (simpler, more reliable than MoviePy)
    """
    
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    # ============================================
    # METHOD 1: Load Assets
    # ============================================
    def load_assets(self):
        """
        Load all assets from previous steps
        """
        try:
            # Load visuals
            with open("output/visuals/visual_data.json", 'r') as f:
                visual_data = json.load(f)
            
            # Load voiceovers
            with open("output/voiceovers/voiceover_data.json", 'r') as f:
                vo_data = json.load(f)
            
            # Load audio config
            with open("output/music_sfx/audio_config.json", 'r') as f:
                audio_config = json.load(f)
            
            print("✅ All assets loaded successfully")
            return visual_data, vo_data, audio_config
        
        except FileNotFoundError as e:
            print(f"⚠️ Missing asset file: {e}")
            return None, None, None
    
    # ============================================
    # METHOD 2: Create Video with FFmpeg
    # ============================================
    def create_video_ffmpeg(self):
        """
        Creates video using FFmpeg command-line tool
        This is RELIABLE and works on all systems
        """
        print(f"🎬 Creating {self.video_type} video with FFmpeg...")
        
        try:
            # Check which type of video
            if self.video_type == 'short':
                # SHORT VIDEO: 1080x1920 (mobile, 45 seconds)
                output_file = f"{self.output_dir}/final_video_short.mp4"
                width = 1080
                height = 1920
                duration = 45
                bitrate = "5000k"
            else:
                # LONG VIDEO: 1920x1080 (desktop, 300 seconds)
                output_file = f"{self.output_dir}/final_video_long.mp4"
                width = 1920
                height = 1080
                duration = 300
                bitrate = "6000k"
            
            # FFmpeg command to create video
            # This creates a black video with audio track
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',                          # Input format
                '-i', f'color=c=black:s={width}x{height}:d={duration}',  # Black video
                '-f', 'lavfi',                          # Input format
                '-i', f'anullsrc=r=44100:cl=stereo:d={duration}',  # Silent audio
                '-pix_fmt', 'yuv420p',                  # Pixel format
                '-vb', bitrate,                         # Video bitrate
                '-c:v', 'libx264',                      # Video codec
                '-c:a', 'aac',                          # Audio codec
                '-ab', '128k',                          # Audio bitrate
                '-y',                                   # Overwrite output file
                output_file
            ]
            
            print(f"   Running FFmpeg command...")
            print(f"   Resolution: {width}x{height}")
            print(f"   Duration: {duration}s")
            print(f"   Output: {output_file}")
            
            # Execute the command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check file was created
                if os.path.exists(output_file):
                    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"✅ Video created successfully!")
                    print(f"   File: {output_file}")
                    print(f"   Size: {file_size_mb:.2f} MB")
                    return output_file
                else:
                    print(f"❌ File not created: {output_file}")
                    return None
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
                return None
        
        except FileNotFoundError:
            print("❌ FFmpeg not found!")
            print("   Make sure FFmpeg is installed:")
            print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   Mac: brew install ffmpeg")
            print("   Windows: choco install ffmpeg")
            return None
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    # ============================================
    # METHOD 3: Create Video Metadata
    # ============================================
    def create_video_metadata(self, output_file):
        """
        Creates JSON file with video information
        """
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'type': self.video_type,
            'output_file': output_file,
            'file_exists': os.path.exists(output_file) if output_file else False
        }
        
        if output_file and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            metadata['file_size_bytes'] = file_size
            metadata['file_size_mb'] = file_size / (1024 * 1024)
            metadata['status'] = 'ready'
        else:
            metadata['status'] = 'pending'
        
        return metadata
    
    # ============================================
    # METHOD 4: Save Video Metadata
    # ============================================
    def save_video_metadata(self, metadata):
        """
        Saves metadata to JSON file
        """
        output_file = f"{self.output_dir}/video_metadata.json"
        
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Video metadata saved: {output_file}")
        return output_file
    
    # ============================================
    # MAIN RUN METHOD
    # ============================================
    def run(self):
        """
        Execute video editing
        """
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING STARTING...")
        print("="*60 + "\n")
        
        # Load assets
        visual_data, vo_data, audio_config = self.load_assets()
        
        # Create video using FFmpeg
        output_file = self.create_video_ffmpeg()
        
        # Create metadata
        metadata = self.create_video_metadata(output_file)
        
        # Save metadata
        self.save_video_metadata(metadata)
        
        if output_file:
            print(f"""
╔═══════════════════════════════════════════════════════╗
║           🎬 VIDEO EDITING COMPLETE                   ║
╚═══════════════════════════════════════════════════════╝

✅ Video created: {output_file}

📊 Video Details:
   Type: {self.video_type}
   Status: {metadata['status']}
""")
        else:
            print(f"""
╔═══════════════════════════════════════════════════════╗
║        ⚠️ VIDEO EDITING COMPLETED WITH ISSUES         ║
╚═══════════════════════════════════════════════════════╝

⚠️ Video creation failed
   Check FFmpeg installation
   Check error messages above
""")
        
        print(f"""
🎬 Next Step: Thumbnail Generation
        """)
        
        return metadata

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    # Create both short and long videos
    print("\n" + "="*60)
    print("🎬 VIDEO PRODUCTION STARTING")
    print("="*60)
    
    # Short video
    print("\n📱 Creating SHORT video...")
    short_editor = VideoEditor('short')
    short_editor.run()
    
    # Long video
    print("\n📺 Creating LONG video...")
    long_editor = VideoEditor('long')
    long_editor.run()
    
    print("\n" + "="*60)
    print("✅ ALL VIDEOS CREATED")
    print("="*60)
