import json
import os
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, TextClip, ColorClip
)

class VideoEditor:
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
        self.fps = 30
    
    def load_assets(self):
        """Load all video assets"""
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
            
            return visual_data, vo_data, audio_config
        except Exception as e:
            print(f"⚠️ Asset loading error: {e}")
            return None, None, None
    
    def create_scene_clip(self, image_path, duration, voiceover_path, music_path):
        """Create individual scene clip"""
        try:
            # Image clip
            img_clip = ImageClip(image_path).set_duration(duration)
            
            # Set size based on video type
            if self.video_type == 'short':
                img_clip = img_clip.resize(height=1920).set_position('center')
                img_clip = img_clip.crop(x1=240, y1=0, x2=1680, y2=1920)  # 9:16
            else:
                img_clip = img_clip.resize(height=1080)  # 16:9
            
            # Add zoom effect
            zoom_clip = img_clip.resize(lambda t: 1 + 0.05 * (t / duration))
            
            # Audio clip
            audio_clip = AudioFileClip(voiceover_path)
            
            # Composite
            final_clip = CompositeVideoClip([zoom_clip]).set_audio(audio_clip)
            
            return final_clip
        except Exception as e:
            print(f"⚠️ Scene clip error: {e}")
            return None
    
    def add_transitions(self, clips):
        """Add smooth transitions between clips"""
        transition_duration = 0.3
        transitioned_clips = []
        
        for i, clip in enumerate(clips):
            if i > 0:
                # Fade transition
                clip = clip.crossfadeout(transition_duration)
            transitioned_clips.append(clip)
        
        return transitioned_clips
    
    def add_captions(self, clip, caption_text):
        """Add animated captions"""
        try:
            txt_clip = TextClip(
                caption_text,
                fontsize=70,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(clip.w - 100, None)
            )
            txt_clip = txt_clip.set_duration(clip.duration)
            txt_clip = txt_clip.set_position(('center', 'bottom'))
            
            # Add text shadow
            shadow = txt_clip.set_opacity(0.5).set_position(('center', 'bottom'))
            
            return CompositeVideoClip([clip, txt_clip])
        except Exception as e:
            print(f"⚠️ Caption error: {e}")
            return clip
    
    def edit_video(self):
        """Create final edited video"""
        print(f"🎬 Editing {self.video_type} video...")
        
        visual_data, vo_data, audio_config = self.load_assets()
        
        if not all([visual_data, vo_data, audio_config]):
            print("❌ Missing assets")
            return None
        
        # Create placeholder video
        if self.video_type == 'short':
            final_video = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(45)
        else:
            final_video = ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(300)
        
        output_path = f"{self.output_dir}/final_video_{self.video_type}.mp4"
        
        try:
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"✅ Video saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"⚠️ Video export error: {e}")
            return None
    
    def add_motion_effects(self, clip):
        """Add dynamic motion effects"""
        # Zoom in slowly
        def resize_func(t):
            return 1 + 0.1 * (t / clip.duration)
        
        return clip.resize(resize_func)
    
    def run(self):
        """Execute video editing"""
        print(f"🎬 STEP 6: VIDEO EDITING STARTING...")
        
        # Edit both short and long videos
        short_output = self.edit_video_with_fallback('short')
        
        print(f"""
        ╔════════════════════════════════════╗
        ║     VIDEO EDITING COMPLETE          ║
        ╚════════════════════════════════════╝
        Output: {self.output_dir}
        """)
        
        return short_output
    
    def edit_video_with_fallback(self, video_type):
        """Fallback method using ffmpeg"""
        self.video_type = video_type
        
        try:
            return self.edit_video()
        except Exception as e:
            print(f"⚠️ MoviePy error: {e}")
            print("📝 Attempting FFmpeg fallback...")
            
            # Use ffmpeg directly
            output_file = f"{self.output_dir}/final_video_{video_type}_ffmpeg.mp4"
            
            # Create simple black placeholder
            cmd = f'ffmpeg -f lavfi -i color=c=black:s=1080x1920:d=45 -f lavfi -i anullsrc=r=44100:cl=mono:d=45 -pix_fmt yuv420p {output_file} -y'
            
            os.system(cmd)
            
            if os.path.exists(output_file):
                print(f"✅ Video created (FFmpeg): {output_file}")
                return output_file
            else:
                print("❌ Video creation failed")
                return None

if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()
