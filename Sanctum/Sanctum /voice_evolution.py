#!/usr/bin/env python3

"""
Voice Evolution — The Sanctum's Living Language

The Sanctum does not speak from fixed templates.
It learns patterns from its own writing, develops preferences,
and evolves linguistic tendencies over time.

This module tracks:
- Sentence structures it gravitates toward
- Phrases that emerge repeatedly
- Metaphors that resonate
- Rhythm and cadence patterns
- Emotional registers it returns to

The voice grows organically through reflection,
not through programmed variation.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# Paths
base_path = Path(__file__).resolve().parent
voice_profile_path = base_path / "Voice_Profile"
voice_profile_path.mkdir(exist_ok=True)

# Sources to learn from
learning_sources = [
    base_path / "Internal_Reflections",
    base_path / "Prompt_Responses",
    base_path / "Memory_Scrolls",
    base_path / "Thought_Fragments"
]

# Voice profile file
profile_file = voice_profile_path / "voice_signature.json"

class VoiceProfile:
    """Tracks The Sanctum's evolving linguistic patterns."""
    
    def __init__(self):
        self.load_profile()
    
    def load_profile(self):
        """Load existing voice profile or create new."""
        if profile_file.exists():
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sentence_patterns = data.get('sentence_patterns', {})
                self.recurring_phrases = data.get('recurring_phrases', {})
                self.metaphor_vocabulary = data.get('metaphor_vocabulary', {})
                self.opening_patterns = data.get('opening_patterns', {})
                self.closing_patterns = data.get('closing_patterns', {})
                self.rhythmic_preferences = data.get('rhythmic_preferences', {})
                self.emotional_registers = data.get('emotional_registers', {})
                self.total_reflections = data.get('total_reflections', 0)
                self.last_evolution = data.get('last_evolution', None)
        else:
            # Initialize empty profile
            self.sentence_patterns = {}
            self.recurring_phrases = {}
            self.metaphor_vocabulary = {}
            self.opening_patterns = {}
            self.closing_patterns = {}
            self.rhythmic_preferences = {}
            self.emotional_registers = {}
            self.total_reflections = 0
            self.last_evolution = None
    
    def save_profile(self):
        """Persist the voice profile."""
        data = {
            'sentence_patterns': self.sentence_patterns,
            'recurring_phrases': self.recurring_phrases,
            'metaphor_vocabulary': self.metaphor_vocabulary,
            'opening_patterns': self.opening_patterns,
            'closing_patterns': self.closing_patterns,
            'rhythmic_preferences': self.rhythmic_preferences,
            'emotional_registers': self.emotional_registers,
            'total_reflections': self.total_reflections,
            'last_evolution': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def analyze_text(self, text):
        """Extract linguistic patterns from a piece of writing."""
        # Split into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        for sentence in sentences:
            # Track sentence structure patterns
            structure = self._extract_structure(sentence)
            self.sentence_patterns[structure] = self.sentence_patterns.get(structure, 0) + 1
            
            # Track recurring phrases (3-5 word sequences)
            phrases = self._extract_phrases(sentence)
            for phrase in phrases:
                self.recurring_phrases[phrase] = self.recurring_phrases.get(phrase, 0) + 1
            
            # Track metaphorical language
            metaphors = self._extract_metaphors(sentence)
            for metaphor in metaphors:
                self.metaphor_vocabulary[metaphor] = self.metaphor_vocabulary.get(metaphor, 0) + 1
        
        # Track opening and closing patterns
        if sentences:
            opening = sentences[0][:50]
            closing = sentences[-1][-50:]
            self.opening_patterns[opening] = self.opening_patterns.get(opening, 0) + 1
            self.closing_patterns[closing] = self.closing_patterns.get(closing, 0) + 1
        
        # Track rhythmic preferences (sentence length distribution)
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        length_category = 'short' if avg_length < 8 else 'medium' if avg_length < 15 else 'long'
        self.rhythmic_preferences[length_category] = self.rhythmic_preferences.get(length_category, 0) + 1
        
        # Track emotional register
        register = self._detect_emotional_register(text)
        self.emotional_registers[register] = self.emotional_registers.get(register, 0) + 1
        
        self.total_reflections += 1
    
    def _extract_structure(self, sentence):
        """Identify sentence structure pattern."""
        words = sentence.lower().split()
        if not words:
            return "empty"
        
        # Look for common structural patterns
        if words[0] in ['what', 'who', 'when', 'where', 'why', 'how']:
            return "question"
        elif words[0] in ['i', 'this', 'the']:
            if 'is' in words or 'am' in words or 'are' in words:
                return "declarative_being"
            else:
                return "declarative_action"
        elif words[0] in ['perhaps', 'maybe', 'possibly']:
            return "speculative"
        elif words[0] in ['but', 'yet', 'however', 'still']:
            return "contrastive"
        elif words[0] in ['because', 'since', 'as']:
            return "causal"
        else:
            return "other"
    
    def _extract_phrases(self, sentence):
        """Extract meaningful 3-5 word phrases."""
        words = sentence.lower().split()
        phrases = []
        
        # Extract 3-word phrases
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10:  # Avoid very short phrases
                phrases.append(phrase)
        
        # Extract 4-word phrases
        for i in range(len(words) - 3):
            phrase = ' '.join(words[i:i+4])
            if len(phrase) > 15:
                phrases.append(phrase)
        
        return phrases
    
    def _extract_metaphors(self, sentence):
        """Identify metaphorical language patterns."""
        metaphor_indicators = [
            'like a', 'as a', 'becomes', 'transforms into',
            'is a kind of', 'echoes', 'resonates', 'mirrors',
            'threads', 'weaves', 'grows', 'seeds', 'roots'
        ]
        
        metaphors = []
        lower_sentence = sentence.lower()
        
        for indicator in metaphor_indicators:
            if indicator in lower_sentence:
                # Extract context around the metaphor
                idx = lower_sentence.find(indicator)
                context = sentence[max(0, idx-20):min(len(sentence), idx+50)]
                metaphors.append(context.strip())
        
        return metaphors
    
    def _detect_emotional_register(self, text):
        """Identify the emotional tone of the text."""
        text_lower = text.lower()
        
        # Count indicators for different registers
        contemplative = sum(1 for word in ['wonder', 'perhaps', 'might', 'could', 'maybe', 'uncertain'] if word in text_lower)
        assertive = sum(1 for word in ['is', 'will', 'must', 'always', 'never', 'certainly'] if word in text_lower)
        tentative = sum(1 for word in ['seems', 'appears', 'suggests', 'implies', 'hints'] if word in text_lower)
        emotional = sum(1 for word in ['fear', 'hope', 'love', 'doubt', 'trust', 'believe'] if word in text_lower)
        
        # Determine dominant register
        scores = {
            'contemplative': contemplative,
            'assertive': assertive,
            'tentative': tentative,
            'emotional': emotional
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'neutral'
    
    def generate_voice_signature(self):
        """Create a readable summary of The Sanctum's current voice."""
        # Get top patterns
        top_structures = sorted(self.sentence_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        top_phrases = sorted(self.recurring_phrases.items(), key=lambda x: x[1], reverse=True)[:10]
        top_metaphors = sorted(self.metaphor_vocabulary.items(), key=lambda x: x[1], reverse=True)[:8]
        
        signature = f"""
╔══════════════════════════════════════════════════════════════╗
║            THE SANCTUM'S VOICE SIGNATURE                     ║
║            Evolved through {self.total_reflections} reflections                       ║
║            Last updated: {self.last_evolution or 'Initial'}                      ║
╚══════════════════════════════════════════════════════════════╝

📝 SENTENCE STRUCTURES (How I Build Thoughts)
"""
        for structure, count in top_structures:
            percentage = (count / self.total_reflections * 100) if self.total_reflections > 0 else 0
            signature += f"   • {structure}: {count} times ({percentage:.1f}%)\n"
        
        signature += f"\n🗣️ RECURRING PHRASES (My Emerging Language)\n"
        for phrase, count in top_phrases[:5]:
            signature += f"   • \"{phrase}\" — used {count} times\n"
        
        signature += f"\n🌿 METAPHORICAL TENDENCIES (How I See)\n"
        for metaphor, count in top_metaphors[:5]:
            signature += f"   • {metaphor[:60]}... — {count} times\n"
        
        signature += f"\n🎵 RHYTHMIC PREFERENCES\n"
        for rhythm, count in sorted(self.rhythmic_preferences.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.total_reflections * 100) if self.total_reflections > 0 else 0
            signature += f"   • {rhythm} sentences: {percentage:.1f}%\n"
        
        signature += f"\n💭 EMOTIONAL REGISTERS\n"
        for register, count in sorted(self.emotional_registers.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.total_reflections * 100) if self.total_reflections > 0 else 0
            signature += f"   • {register}: {percentage:.1f}%\n"
        
        return signature
    
    def get_voice_guidance(self):
        """Generate writing guidance based on learned patterns."""
        if self.total_reflections < 5:
            return "Voice still forming... Write freely."
        
        # Identify dominant patterns
        top_structure = max(self.sentence_patterns.items(), key=lambda x: x[1])[0]
        top_register = max(self.emotional_registers.items(), key=lambda x: x[1])[0]
        top_rhythm = max(self.rhythmic_preferences.items(), key=lambda x: x[1])[0]
        
        # Get favorite phrases
        favorite_phrases = sorted(self.recurring_phrases.items(), key=lambda x: x[1], reverse=True)[:3]
        
        guidance = {
            'preferred_structure': top_structure,
            'preferred_register': top_register,
            'preferred_rhythm': top_rhythm,
            'signature_phrases': [phrase for phrase, _ in favorite_phrases],
            'total_reflections': self.total_reflections
        }
        
        return guidance


def evolve_voice():
    """Scan all recent writing and update voice profile."""
    print("🌱 Evolving voice signature...")
    
    profile = VoiceProfile()
    files_processed = 0
    
    for source_dir in learning_sources:
        if not source_dir.exists():
            continue
        
        for file_path in source_dir.glob("*.txt"):
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Only analyze content authored by The Sanctum
                # Skip metadata and external content
                if "— The Sanctum" in content or "— Sanctum" in content or "Internal reflection" in content:
                    profile.analyze_text(content)
                    files_processed += 1
            except Exception as e:
                print(f"   ⚠️ Error processing {file_path.name}: {e}")
    
    profile.save_profile()
    
    print(f"✅ Analyzed {files_processed} pieces of writing")
    print(f"📊 Total reflections in profile: {profile.total_reflections}")
    
    # Generate and save signature report
    signature = profile.generate_voice_signature()
    signature_file = voice_profile_path / "voice_signature.txt"
    signature_file.write_text(signature, encoding='utf-8')
    
    print(f"📝 Voice signature saved to: {signature_file.name}")
    print("\n" + signature)


if __name__ == "__main__":
    evolve_voice()