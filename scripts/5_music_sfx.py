import json
import os
import requests

class MusicSoundGenerator:
    def __init__(self):
        self.output_dir = "output/music_sfx"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_free_music_libraries(self):
        """List of free music sources"""
        return {
            'pixabay': 'https://pixabay.com/music/search/',
            'freepd': 'https://freepd.com/',
            'incompetech': 'http://incompetech.com/music/',
            'youtube_audio_library': 'https://www.youtube.com/audiolibrary',
            'bensound': 'https://www.bensound.com/',
            'ccmixter': 'http://ccmixter.org/'
        }
    
    def download_free_music(self, genre, mood):
        """Download copyright-free music"""
        # Placeholder music download logic
        music_files = {
            'suspenseful': 'suspense_background.mp3',
            'dramatic': 'dramatic_orchestral.mp3',
            'emotional': 'emotional_strings.mp3',
            'action': 'action_drums.mp3',
            'calm': 'calm_ambient.mp3'
        }
        
        # Create placeholder files
        music_file = f"{self.output_dir}/{mood}_music.mp3"
        
        # Touch file to create placeholder
        open(music_file, 'a').close()
        
        print(f"✅ Music file: {music_file}")
        return music_file
    
    def get_sound_effects(self):
        """Get free sound effects"""
        sfx_sources = {
            'freesound': 'https://freesound.org/',
            'zapsplat': 'https://www.zapsplat.com/',
            'sound_bible': 'http://soundbible.com/',
            'epidemic': 'https://www.epidemicsound.com/free-sounds/'
        }
        
        return sfx_sources
    
    def select_music_for_scene(self, scene_mood):
        """Select appropriate music for scene"""
        mood_to_music = {
            'suspenseful': 'suspenseful buildup',
            'dramatic': 'dramatic orchestral',
            'emotional': 'emotional strings',
            'action': 'action drums',
            'calm': 'calm ambient'
        }
        
        return mood_to_music.get(scene_mood, 'calm ambient')
    
    def add_sfx_timing(self, script):
        """Add sound effect timing"""
        sfx_schedule = []
        
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                script_data = json.load(f)
                
                for scene in script_data.get('scenes', []):
                    sfx_schedule.append({
                        'scene': scene.get('scene'),
                        'start_time': sum([s.get('duration', 0) for s in script_data['scenes'][:scene.get('scene')-1]]),
                        'duration': scene.get('duration'),
                        'sound_effect': 'transition whoosh'
                    })
        except:
            pass
        
        return sfx_schedule
    
    def create_audio_mix(self):
        """Create balanced audio mix"""
        # Background: 40% volume
        # Voiceover: 100% volume
        # SFX: 60% volume
        
        mix_config = {
            'background_music': {'volume': 0.4, 'fade_in': 1.0, 'fade_out': 2.0},
            'voiceover': {'volume': 1.0, 'normalization': True},
            'sound_effects': {'volume': 0.6, 'compression': True}
        }
        
        return mix_config
    
    def save_audio_config(self, music_file, sfx_schedule, mix_config):
        """Save audio configuration"""
        data = {
            'background_music': music_file,
            'sfx_schedule': sfx_schedule,
            'mix_configuration': mix_config
        }
        
        with open(f"{self.output_dir}/audio_config.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def run(self):
        """Generate music and SFX"""
        print("🎵 STEP 5: MUSIC & SFX GENERATION STARTING...")
        
        # Download music
        music_file = self.download_free_music('cinematic', 'suspenseful')
        
        # Schedule SFX
        sfx_schedule = self.add_sfx_timing({})
        
        # Create mix
        mix_config = self.create_audio_mix()
        
        # Save
        audio_data = self.save_audio_config(music_file, sfx_schedule, mix_config)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║    MUSIC & SFX CONFIGURED           ║
        ╚════════════════════════════════════╝
        Background Music: {music_file}
        Sound Effects: {len(sfx_schedule)} scheduled
        """)
        
        return audio_data

if __name__ == "__main__":
    generator = MusicSoundGenerator()
    generator.run()
