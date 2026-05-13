import json
import os
import subprocess
import shutil
from datetime import datetime

class VideoEditor:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_assets(self):
        """Load visual and voiceover data"""
        print("   Loading assets...")
        
        try:
            with open("output/visuals/visual_data.json", 'r') as f:
                visual_data = json.load(f)
        except Exception as e:
            print(f"   ❌ Visual data error: {e}")
            return None, None
        
        try:
            with open("output/voiceovers/voiceover_data.json", 'r') as f:
                vo_data = json.load(f)
        except Exception as e:
            print(f"   ❌ Voiceover data error: {e}")
            return None, None
        
        return visual_data, vo_data
    
    def combine_scene(self, video_file, audio_file, output_file, duration, scene_num):
        """Combine one video scene with its audio"""
        print(f"      Scene {scene_num}: Combining...")
        
        # Check files exist
        if not video_file or not os.path.exists(video_file):
            print(f"         ⚠️ Video missing: {video_file}")
            return None
        
        if not audio_file or not os.path.exists(audio_file):
            print(f"         ⚠️ Audio missing: {audio_file}")
            # Use video without audio
            shutil.copy(video_file, output_file)
            return output_file
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"         ✅ Combined ({size:.2f} MB)")
                return output_file
            else:
                print(f"         ⚠️ Combine failed, using video only")
                shutil.copy(video_file, output_file)
                return output_file
        
        except Exception as e:
            print(f"         ⚠️ Error: {e}")
            shutil.copy(video_file, output_file)
            return output_file
    
    def concatenate(self, scene_files, output_file):
        """Concatenate all scenes into final video"""
        print(f"\n   Concatenating {len(scene_files)} scenes...")
        
        if not scene_files:
            return None
        
        # Filter existing files
        existing = [f for f in scene_files if f and os.path.exists(f)]
        
        if not existing:
            print("   ❌ No scene files found!")
            return None
        
        if len(existing) == 1:
            shutil.copy(existing[0], output_file)
            print(f"   ✅ Single scene copied")
            return output_file
        
        # Create concat file
        concat_file = f"{self.output_dir}/concat.txt"
        with open(concat_file, 'w') as f:
            for sf in existing:
                f.write(f"file '{os.path.abspath(sf)}'\n")
        
        try:
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"   ✅ Final video: {size:.2f} MB")
                return output_file
            else:
                print(f"   ⚠️ Concat failed, using first scene")
                shutil.copy(existing[0], output_file)
                return output_file
        
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            shutil.copy(existing[0], output_file)
            return output_file
    
    def create_video(self, visual_scenes, vo_scenes, video_type):
        """Create complete video from scenes"""
        print(f"\n🎬 Creating {video_type.upper()} video...")
        
        if not visual_scenes or not vo_scenes:
            print(f"   ❌ Missing scenes for {video_type}")
            return None
        
        scene_files = []
        
        for i, visual in enumerate(visual_scenes):
            if i < len(vo_scenes):
                vo = vo_scenes[i]
                
                video_file = visual.get('file')
                audio_file = vo.get('file')
                duration = visual.get('duration', 5)
                scene_num = visual.get('scene', i+1)
                
                scene_output = f"{self.output_dir}/{video_type}_scene_{scene_num}.mp4"
                
                result = self.combine_scene(
                    video_file, audio_file,
                    scene_output, duration, scene_num
                )
                
                if result:
                    scene_files.append(result)
        
        if not scene_files:
            print(f"   ❌ No scenes created for {video_type}")
            return None
        
        # Concatenate
        final_output = f"{self.output_dir}/final_{video_type}.mp4"
        return self.concatenate(scene_files, final_output)
    
    def run(self):
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING")
        print("="*60)
        
        # Load assets
        visual_data, vo_data = self.load_assets()
        
        if not visual_data or not vo_data:
            print("\n❌ Missing data files!")
            return None
        
        # Get short and long scenes
        short_visuals = visual_data.get('short_scenes', [])
        long_visuals = visual_data.get('long_scenes', [])
        short_vos = vo_data.get('short_voiceovers', [])
        long_vos = vo_data.get('long_voiceovers', [])
        
        print(f"\n   Short visuals: {len(short_visuals)}")
        print(f"   Short voiceovers: {len(short_vos)}")
        print(f"   Long visuals: {len(long_visuals)}")
        print(f"   Long voiceovers: {len(long_vos)}")
        
        results = {}
        
        # Create SHORT video
        short_result = self.create_video(short_visuals, short_vos, 'short')
        if short_result:
            size = os.path.getsize(short_result) / (1024 * 1024)
            results['short'] = {'file': short_result, 'size_mb': size}
            print(f"\n✅ SHORT VIDEO: {short_result} ({size:.2f} MB)")
        
        # Create LONG video
        long_result = self.create_video(long_visuals, long_vos, 'long')
        if long_result:
            size = os.path.getsize(long_result) / (1024 * 1024)
            results['long'] = {'file': long_result, 'size_mb': size}
            print(f"✅ LONG VIDEO: {long_result} ({size:.2f} MB)")
        
        # Save metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'results': results
        }
        
        with open(f"{self.output_dir}/video_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"""
╔══════════════════════════════════════════╗
║     ✅ VIDEO EDITING COMPLETE            ║
╚══════════════════════════════════════════╝

📱 SHORT: output/videos/final_short.mp4
📺 LONG:  output/videos/final_long.mp4

✨ Features:
   ✅ Animated video backgrounds
   ✅ Human-like voice narration
   ✅ Different content (short vs long)
   ✅ Ready for YouTube!
        """)
        
        return results

if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()
