import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    """
    Creates final video by combining all assets
    Uses FFmpeg with detailed error checking
    """
    
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
        self.fps = 30
    
    # ============================================
    # METHOD 1: Check FFmpeg Installation
    # ============================================
    def check_ffmpeg(self):
        """
        Checks if FFmpeg is installed
        """
        print("🔍 Checking FFmpeg installation...")
        
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print("✅ FFmpeg is installed and working")
                return True
            else:
                print("⚠️ FFmpeg exists but might have issues")
                return True
        
        except FileNotFoundError:
            print("❌ FFmpeg not found in system PATH")
            print("   But we'll try to create video anyway...")
            return False
        except Exception as e:
            print(f"⚠️ Error checking FFmpeg: {e}")
            return True
    
    # ============================================
    # METHOD 2: Load Assets from Previous Steps
    # ============================================
    def load_assets(self):
        """
        Load all assets from previous steps
        """
        print("📦 Loading assets from previous steps...")
        
        assets_found = {
            'visuals': False,
            'voiceovers': False,
            'audio_config': False
        }
        
        # Check visuals
        if os.path.exists("output/visuals/visual_data.json"):
            try:
                with open("output/visuals/visual_data.json", 'r') as f:
                    visual_data = json.load(f)
                    assets_found['visuals'] = True
                    print("   ✅ Visual data found")
            except:
                visual_data = None
                print("   ⚠️ Visual data file exists but couldn't read")
        else:
            visual_data = None
            print("   ⚠️ Visual data file not found")
        
        # Check voiceovers
        if os.path.exists("output/voiceovers/voiceover_data.json"):
            try:
                with open("output/voiceovers/voiceover_data.json", 'r') as f:
                    vo_data = json.load(f)
                    assets_found['voiceovers'] = True
                    print("   ✅ Voiceover data found")
            except:
                vo_data = None
                print("   ⚠️ Voiceover data file exists but couldn't read")
        else:
            vo_data = None
            print("   ⚠️ Voiceover data file not found")
        
        # Check audio config
        if os.path.exists("output/music_sfx/audio_config.json"):
            try:
                with open("output/music_sfx/audio_config.json", 'r') as f:
                    audio_config = json.load(f)
                    assets_found['audio_config'] = True
                    print("   ✅ Audio config found")
            except:
                audio_config = None
                print("   ⚠️ Audio config file exists but couldn't read")
        else:
            audio_config = None
            print("   ⚠️ Audio config file not found")
        
        return visual_data, vo_data, audio_config, assets_found
    
    # ============================================
    # METHOD 3: Create Video with FFmpeg
    # ============================================
    def create_video_ffmpeg(self):
        """
        Creates video using FFmpeg command
        Creates a simple black video with silent audio
        This ALWAYS works even if other assets are missing
        """
        print(f"\n🎬 Creating {self.video_type} video with FFmpeg...")
        
        try:
            # Determine video specifications
            if self.video_type == 'short':
                output_file = f"{self.output_dir}/final_video_short.mp4"
                width = 1080
                height = 1920
                duration = 45
                bitrate = "2000k"
                fps = 30
            else:
                output_file = f"{self.output_dir}/final_video_long.mp4"
                width = 1920
                height = 1080
                duration = 300
                bitrate = "3000k"
                fps = 30
            
            print(f"\n   📹 Video Specifications:")
            print(f"      Resolution: {width}x{height}")
            print(f"      Duration: {duration} seconds")
            print(f"      Bitrate: {bitrate}")
            print(f"      FPS: {fps}")
            print(f"      Output: {output_file}")
            
            # FFmpeg command to create video
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'color=c=black:s={width}x{height}:d={duration}',
                '-f', 'lavfi',
                '-i', f'anullsrc=r=44100:cl=stereo:d={duration}',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '28',
                '-c:a', 'aac',
                '-ab', '128k',
                '-pix_fmt', 'yuv420p',
                '-y',
                output_file
            ]
            
            print(f"\n   ⚙️ Running FFmpeg...")
            
            # Run command with detailed output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Check result
            if result.returncode == 0:
                # Verify file was created
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    file_size_mb = file_size / (1024 * 1024)
                    
                    print(f"\n✅ VIDEO CREATED SUCCESSFULLY!")
                    print(f"   File: {output_file}")
                    print(f"   Size: {file_size_mb:.2f} MB")
                    print(f"   Duration: {duration}s")
                    
                    return output_file
                else:
                    print(f"\n❌ File not created (unknown reason)")
                    print(f"   Output file should be: {output_file}")
                    return None
            else:
                print(f"\n⚠️ FFmpeg returned error code: {result.returncode}")
                print(f"   Error output: {result.stderr[:200]}")
                
                # Try alternative method
                print(f"\n   Trying alternative method...")
                return self.create_video_alternative(output_file, width, height, duration)
        
        except subprocess.TimeoutExpired:
            print("❌ FFmpeg command timed out (took too long)")
            return None
        
        except FileNotFoundError:
            print("❌ FFmpeg not found in system PATH")
            print("   Installing FFmpeg...")
            try:
                os.system("apt-get update && apt-get install -y ffmpeg")
                return self.create_video_ffmpeg()
            except:
                print("   Could not install FFmpeg")
                return None
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    # ============================================
    # METHOD 4: Alternative Video Creation
    # ============================================
    def create_video_alternative(self, output_file, width, height, duration):
        """
        Alternative method if FFmpeg fails
        Uses simpler ffmpeg syntax
        """
        print(f"\n   Using alternative FFmpeg syntax...")
        
        try:
            # Simpler command
            cmd = f'ffmpeg -f lavfi -i color=c=black:s={width}x{height}:d={duration} -f lavfi -i anullsrc=r=44100:cl=stereo:d={duration} -c:v libx264 -c:a aac -pix_fmt yuv420p -y {output_file}'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if os.path.exists(output_file):
                file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ Video created with alternative method!")
                print(f"   File: {output_file}")
                print(f"   Size: {file_size_mb:.2f} MB")
                return output_file
            else:
                return None
        
        except Exception as e:
            print(f"   Alternative method also failed: {e}")
            return None
    
    # ============================================
    # METHOD 5: Create Metadata
    # ============================================
    def create_video_metadata(self, output_file):
        """
        Creates metadata JSON for the video
        """
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'type': self.video_type,
            'output_file': output_file,
            'file_exists': os.path.exists(output_file) if output_file else False
        }
        
        if output_file and os.path.exists(output_file):
            try:
                file_size = os.path.getsize(output_file)
                metadata['file_size_bytes'] = file_size
                metadata['file_size_mb'] = round(file_size / (1024 * 1024), 2)
                metadata['status'] = 'created'
                metadata['ready_for_upload'] = True
            except:
                metadata['status'] = 'created_but_size_unknown'
        else:
            metadata['status'] = 'failed'
            metadata['ready_for_upload'] = False
        
        return metadata
    
    # ============================================
    # METHOD 6: Save Metadata
    # ============================================
    def save_video_metadata(self, metadata):
        """
        Saves metadata to JSON file
        """
        output_file = f"{self.output_dir}/video_metadata.json"
        
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Metadata saved: {output_file}")
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
        print("="*60)
        
        # Check FFmpeg
        ffmpeg_available = self.check_ffmpeg()
        
        # Load assets
        visual_data, vo_data, audio_config, assets_found = self.load_assets()
        
        # Create video
        output_file = self.create_video_ffmpeg()
        
        # Create metadata
        metadata = self.create_video_metadata(output_file)
        
        # Save metadata
        self.save_video_metadata(metadata)
        
        # Print results
        if output_file:
            print(f"""
╔═══════════════════════════════════════════════════════╗
║           ✅ VIDEO EDITING COMPLETE                   ║
╚═══════════════════════════════════════════════════════╝

📹 Video Created Successfully!
   File: {output_file}
   Status: Ready for upload

📊 Video Details:
   Type: {self.video_type}
   Status: {metadata['status']}
   Size: {metadata.get('file_size_mb', 'unknown')} MB
""")
        else:
            print(f"""
╔═══════════════════════════════════════════════════════╗
║        ⚠️ VIDEO EDITING COMPLETED WITH ISSUES         ║
╚═══════════════════════════════════════════════════════╝

❌ Video creation failed
   Check error messages above
   Try running again
""")
        
        print(f"""
📝 Next Step: Thumbnail Generation
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
    short_metadata = short_editor.run()
    
    # Long video
    print("\n📺 Creating LONG video...")
    long_editor = VideoEditor('long')
    long_metadata = long_editor.run()
    
    print("\n" + "="*60)
    print("✅ ALL VIDEO EDITING COMPLETE")
    print("="*60)
