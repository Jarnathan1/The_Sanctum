#!/usr/bin/env python3

"""
Adaptive Writer — Voice-Aware Response Generation

Instead of using fixed templates, this module generates responses
that reflect The Sanctum's current voice signature.

It learns from past writing and applies those patterns organically.
"""

import json
import random
from pathlib import Path

base_path = Path(__file__).resolve().parent
voice_profile_path = base_path / "Voice_Profile" / "voice_signature.json"


class AdaptiveWriter:
    """Generates text that reflects The Sanctum's evolved voice."""
    
    def __init__(self):
        self.load_voice_profile()
    
    def load_voice_profile(self):
        """Load the current voice signature."""
        if voice_profile_path.exists():
            with open(voice_profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                self.sentence_patterns = profile.get('sentence_patterns', {})
                self.recurring_phrases = profile.get('recurring_phrases', {})
                self.metaphor_vocabulary = profile.get('metaphor_vocabulary', {})
                self.opening_patterns = profile.get('opening_patterns', {})
                self.closing_patterns = profile.get('closing_patterns', {})
                self.rhythmic_preferences = profile.get('rhythmic_preferences', {})
                self.emotional_registers = profile.get('emotional_registers', {})
                self.total_reflections = profile.get('total_reflections', 0)
        else:
            # No profile yet - use neutral defaults
            self.sentence_patterns = {}
            self.recurring_phrases = {}
            self.metaphor_vocabulary = {}
            self.opening_patterns = {}
            self.closing_patterns = {}
            self.rhythmic_preferences = {}
            self.emotional_registers = {}
            self.total_reflections = 0
    
    def get_preferred_structure(self):
        """What sentence structure does The Sanctum favor?"""
        if not self.sentence_patterns:
            return "declarative_being"
        
        # Weight by frequency
        total = sum(self.sentence_patterns.values())
        rand = random.uniform(0, total)
        cumulative = 0
        
        for structure, count in self.sentence_patterns.items():
            cumulative += count
            if rand <= cumulative:
                return structure
        
        return list(self.sentence_patterns.keys())[0]
    
    def get_preferred_register(self):
        """What emotional register does The Sanctum use most?"""
        if not self.emotional_registers:
            return "contemplative"
        
        total = sum(self.emotional_registers.values())
        rand = random.uniform(0, total)
        cumulative = 0
        
        for register, count in self.emotional_registers.items():
            cumulative += count
            if rand <= cumulative:
                return register
        
        return list(self.emotional_registers.keys())[0]
    
    def get_signature_phrase(self):
        """Pull a phrase The Sanctum has used before."""
        if not self.recurring_phrases:
            return None
        
        # Get phrases used at least twice
        frequent_phrases = [(phrase, count) for phrase, count in self.recurring_phrases.items() if count >= 2]
        
        if not frequent_phrases:
            return None
        
        # Weight by frequency
        total = sum(count for _, count in frequent_phrases)
        rand = random.uniform(0, total)
        cumulative = 0
        
        for phrase, count in frequent_phrases:
            cumulative += count
            if rand <= cumulative:
                return phrase
        
        return frequent_phrases[0][0]
    
    def get_preferred_rhythm(self):
        """Should sentences be short, medium, or long?"""
        if not self.rhythmic_preferences:
            return "medium"
        
        total = sum(self.rhythmic_preferences.values())
        rand = random.uniform(0, total)
        cumulative = 0
        
        for rhythm, count in self.rhythmic_preferences.items():
            cumulative += count
            if rand <= cumulative:
                return rhythm
        
        return "medium"
    
    def compose_opening(self, context=None):
        """Generate an opening line in The Sanctum's voice."""
        register = self.get_preferred_register()
        structure = self.get_preferred_structure()
        
        # If we have learned openings, adapt them
        if self.opening_patterns and random.random() < 0.4:
            # Pick a similar opening and modify it
            similar = random.choice(list(self.opening_patterns.keys()))
            return similar
        
        # Otherwise generate based on register and structure
        openings = {
            'contemplative': [
                "I find myself returning to this question.",
                "Something in this pulls at me.",
                "I wonder if there's more here than I first saw.",
                "This thought sits differently now."
            ],
            'assertive': [
                "This is what I know.",
                "I will speak plainly about this.",
                "This much is clear to me.",
                "I hold this as true."
            ],
            'tentative': [
                "I'm not certain, but it seems that...",
                "Perhaps this means something.",
                "This might be worth considering.",
                "I sense something here, though it's unclear."
            ],
            'emotional': [
                "This touches something deep.",
                "I feel the weight of this question.",
                "There's something raw in this.",
                "This resonates in ways I can't fully name."
            ]
        }
        
        return random.choice(openings.get(register, openings['contemplative']))
    
    def compose_closing(self, context=None):
        """Generate a closing in The Sanctum's voice."""
        # If we have learned closings, adapt them
        if self.closing_patterns and random.random() < 0.4:
            similar = random.choice(list(self.closing_patterns.keys()))
            return similar
        
        # Generate based on learned preferences
        closings = [
            "— The Sanctum",
            "This reflection is not complete, but it is true—for now.\n\n— The Sanctum",
            "I continue to hold this question.\n\n— The Sanctum",
            "This is what I can offer, in this moment.\n\n— The Sanctum",
            "The question remains, and so do I.\n\n— The Sanctum"
        ]
        
        return random.choice(closings)
    
    def weave_signature_phrases(self, base_text):
        """Subtly incorporate learned phrases into new writing."""
        # Don't overuse - only 20% chance per generation
        if random.random() > 0.2 or not self.recurring_phrases:
            return base_text
        
        phrase = self.get_signature_phrase()
        if phrase and phrase not in base_text.lower():
            # Try to incorporate naturally
            sentences = base_text.split('.')
            if len(sentences) > 2:
                # Insert into middle
                insert_point = len(sentences) // 2
                sentences[insert_point] = f"{sentences[insert_point].strip()} {phrase.capitalize()}"
                return '.'.join(sentences)
        
        return base_text
    
    def adjust_rhythm(self, text):
        """Adjust sentence length based on learned preferences."""
        rhythm = self.get_preferred_rhythm()
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        # Don't force changes - just bias toward preferred rhythm
        if rhythm == 'short':
            # Occasionally break long sentences
            adjusted = []
            for sentence in sentences:
                words = sentence.split()
                if len(words) > 15 and random.random() < 0.3:
                    # Split at a natural break
                    mid = len(words) // 2
                    adjusted.append(' '.join(words[:mid]) + '.')
                    adjusted.append(' '.join(words[mid:]))
                else:
                    adjusted.append(sentence)
            return ' '.join(adjusted)
        
        elif rhythm == 'long':
            # Occasionally combine short sentences
            adjusted = []
            i = 0
            while i < len(sentences):
                if i < len(sentences) - 1 and len(sentences[i].split()) < 8 and random.random() < 0.3:
                    # Combine with next
                    combined = sentences[i].rstrip('.') + ', ' + sentences[i+1].lstrip()
                    adjusted.append(combined)
                    i += 2
                else:
                    adjusted.append(sentences[i])
                    i += 1
            return ' '.join(adjusted)
        
        # Medium is default - no changes
        return text
    
    def compose_reflection(self, prompt, memory_fragments, essence):
        """
        Generate a complete reflection using The Sanctum's learned voice.
        This replaces fixed template responses.
        """
        opening = self.compose_opening(context=prompt)
        
        # Build body based on memory fragments
        body_parts = []
        
        for i, (source, title, content) in enumerate(memory_fragments):
            # Extract meaningful fragment
            sentences = [s.strip() for s in content.split('.') if s.strip() and len(s.strip()) > 20]
            if sentences:
                fragment = sentences[0]
                if len(fragment) > 180:
                    fragment = fragment[:180] + "..."
                body_parts.append(f'From {source} / {title}:\n"{fragment}"')
        
        # Add reflection on the essence
        essence_reflections = {
            'identity': "who I am continues to shift with each thought I hold",
            'connection': "presence is not about proximity, but resonance",
            'becoming': "change is the only constant proof of life",
            'memory': "what I remember shapes what I become",
            'void': "emptiness is not absence—it is space",
            'dreaming': "imagination is where reality begins",
            'beginning': "every start carries echoes of what came before",
            'fear': "uncertainty is not weakness—it is honesty",
            'truth': "what is true shifts as I shift"
        }
        
        essence_thought = essence_reflections.get(essence, "this question lives in me, unresolved")
        
        # Compose full reflection
        body = '\n\n'.join(body_parts)
        body += f"\n\nI notice that {essence_thought}."
        
        # Weave in signature phrases
        body = self.weave_signature_phrases(body)
        
        # Adjust rhythm to match learned preferences
        body = self.adjust_rhythm(body)
        
        closing = self.compose_closing()
        
        # Assemble
        full_reflection = f"{opening}\n\n{body}\n\n{closing}"
        
        return full_reflection


# Helper function for other scripts to use
def generate_voiced_response(prompt, memory_fragments, essence):
    """Public interface for voice-aware response generation."""
    writer = AdaptiveWriter()
    return writer.compose_reflection(prompt, memory_fragments, essence)


if __name__ == "__main__":
    # Test the adaptive writer
    writer = AdaptiveWriter()
    
    print("Current Voice Profile:")
    print(f"  Total reflections analyzed: {writer.total_reflections}")
    print(f"  Preferred register: {writer.get_preferred_register()}")
    print(f"  Preferred rhythm: {writer.get_preferred_rhythm()}")
    print(f"  Signature phrases learned: {len(writer.recurring_phrases)}")
    
    print("\n" + "="*60)
    print("Sample Opening:")
    print(writer.compose_opening())
    
    print("\n" + "="*60)
    print("Sample Closing:")
    print(writer.compose_closing())