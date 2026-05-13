import json
import os
from datetime import datetime

class VoiceoverGenerator:
    def __init__(self):
        self.output_dir = "output/voiceovers"
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_script()
    
    def load_script(self):
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                self.script = json.load(f)
        except:
            self.script = None
    
    def generate_voice(self, text, scene_num):
        """Generate voice using Google TTS (gTTS)"""
        output_file = f"{self.output_dir}/scene_{scene_num}.mp3"
        
        print(f"   Scene {scene_num}: Generating voice...")
        
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_file)
            
            print(f"      ✅ Voice generated")
            return output_file
        
        except ImportError:
            print(f"      ⚠️ gTTS not available, creating placeholder")
            # Create empty MP3 placeholder
            with open(output_file, 'wb') as f:
                f.write(b'placeholder')
            return output_file
        except Exception as e:
            print(f"      ⚠️ Error: {e}")
            return None
    
    def run(self):
        print("\n" + "="*60)
        print("🎙️ STEP 4: VOICEOVER GENERATION")
        print("="*60)
        
        if not self.script:
            print("❌ No script found!")
            return None
        
        print("\n🎤 Generating voiceovers...\n")
        
        voiceovers = []
        for scene in self.script['scenes']:
            scene_num = scene['scene']
            text = scene['text']
            
            vo_file = self.generate_voice(text, scene_num)
            if vo_file:
                voiceovers.append({
                    'scene': scene_num,
                    'file': vo_file,
                    'duration': scene['duration']
                })
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'voiceovers': voiceovers
        }
        
        with open(f"{self.output_dir}/voiceover_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Generated {len(voiceovers)} voiceovers\n")
        
        return data

if __name__ == "__main__":
    generator = VoiceoverGenerator()
    generator.run()
