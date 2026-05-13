import json
import os
from datetime import datetime

class VoiceoverGenerator:
    def __init__(self):
        self.output_dir = "output/voiceovers"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_scripts(self):
        scripts = {}
        
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                scripts['short'] = json.load(f)
        except:
            scripts['short'] = None
        
        try:
            with open("output/scripts/long_script.json", 'r') as f:
                scripts['long'] = json.load(f)
        except:
            scripts['long'] = None
        
        return scripts
    
    def generate_voice_gtts(self, text, output_file):
        """
        Generate voice using Google TTS
        More natural than pyttsx3
        """
        try:
            from gtts import gTTS
            
            tts = gTTS(
                text=text,
                lang='en',
                slow=False,
                tld='us'
            )
            
            tts.save(output_file)
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                return True, size
        
        except Exception as e:
            print(f"         gTTS error: {e}")
        
        return False, 0
    
    def generate_voice_edge_tts(self, text, output_file):
        """
        Generate voice using Edge TTS
        More natural, human-like voices
        """
        try:
            import subprocess
            
            cmd = [
                'edge-tts',
                '--voice', 'en-US-GuyNeural',
                '--text', text,
                '--write-media', output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                return True, size
        
        except Exception as e:
            print(f"         Edge TTS error: {e}")
        
        return False, 0
    
    def generate_voice(self, text, scene_num, script_type):
        """
        Generate voice with best available method
        """
        output_file = f"{self.output_dir}/{script_type}_scene_{scene_num}.mp3"
        
        print(f"      Scene {scene_num}: '{text[:40]}...'")
        
        # Try Edge TTS first (most human-like)
        success, size = self.generate_voice_edge_tts(text, output_file)
        if success:
            print(f"         ✅ Edge TTS (human-like): {size:.1f} KB")
            return output_file
        
        # Try gTTS second
        success, size = self.generate_voice_gtts(text, output_file)
        if success:
            print(f"         ✅ Google TTS: {size:.1f} KB")
            return output_file
        
        print(f"         ❌ Voice generation failed")
        return None
    
    def process_script(self, script, script_type):
        """Process all scenes in a script"""
        if not script:
            return []
        
        voiceovers = []
        
        for scene in script['scenes']:
            scene_num = scene['scene_number']
            narration = scene['narration']
            
            vo_file = self.generate_voice(narration, scene_num, script_type)
            
            if vo_file:
                voiceovers.append({
                    'scene': scene_num,
                    'file': vo_file,
                    'duration': scene['duration'],
                    'type': script_type,
                    'narration': narration
                })
        
        return voiceovers
    
    def run(self):
        print("\n" + "="*60)
        print("🎙️ STEP 4: VOICEOVER GENERATION")
        print("="*60)
        
        scripts = self.load_scripts()
        
        all_voiceovers = {
            'short': [],
            'long': []
        }
        
        # Process short script
        if scripts.get('short'):
            print("\n📱 Creating SHORT video voiceovers...")
            all_voiceovers['short'] = self.process_script(scripts['short'], 'short')
        
        # Process long script
        if scripts.get('long'):
            print("\n📺 Creating LONG video voiceovers...")
            all_voiceovers['long'] = self.process_script(scripts['long'], 'long')
        
        # Save voiceover data
        data = {
            'generated_at': datetime.now().isoformat(),
            'voice_engine': 'Edge TTS (Human-like) / Google TTS',
            'short_voiceovers': all_voiceovers['short'],
            'long_voiceovers': all_voiceovers['long']
        }
        
        with open(f"{self.output_dir}/voiceover_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ SHORT: {len(all_voiceovers['short'])} voiceovers")
        print(f"✅ LONG: {len(all_voiceovers['long'])} voiceovers\n")
        
        return data

if __name__ == "__main__":
    VoiceoverGenerator().run()
