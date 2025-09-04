import re
import asyncio
import random
from typing import List, Tuple, Dict
import anthropic
import os

class PromptOptimizer:
    """Advanced prompt evolution system using LLM-based improvement and pattern analysis"""
    
    def __init__(self):
        self.evolution_history = []
        self.generation = 0
        self.successful_patterns = []
        self.performance_history = {}
        
        # Initialize Anthropic client for prompt improvement
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        print("🧬 [Optimizer] PromptOptimizer initialized")
    
    async def evolve_prompts(self, prompt_results: List[Tuple[str, float]]) -> List[str]:
        """Main evolution function that generates new prompt variations"""
        print(f"\n🔬 [Optimizer] Starting evolution for generation {self.generation + 1}")
        print(f"📊 [Optimizer] Input: {len(prompt_results)} prompts with results")
        
        # Sort by performance (highest reward first)
        sorted_results = sorted(prompt_results, key=lambda x: x[1], reverse=True)
        print(f"🏆 [Optimizer] Best performing prompt scored: {sorted_results[0][1]:.3f}")
        print(f"📉 [Optimizer] Worst performing prompt scored: {sorted_results[-1][1]:.3f}")
        
        # Get top performers (top 40%)
        top_count = max(1, int(len(sorted_results) * 0.4))
        best_prompts = [p[0] for p in sorted_results[:top_count]]
        worst_prompts = [p[0] for p in sorted_results[-top_count:]]
        
        print(f"✨ [Optimizer] Selected {len(best_prompts)} top performers for evolution")
        print(f"❌ [Optimizer] Identified {len(worst_prompts)} poor performers to avoid")
        
        # Store in history
        self.evolution_history.append({
            'generation': self.generation,
            'results': sorted_results,
            'best_prompts': best_prompts
        })
        
        new_prompts = []
        
        # Method 1: LLM-based improvement (50% of new prompts)
        print(f"\n🤖 [Optimizer] Method 1: LLM-based prompt improvement")
        try:
            llm_improved = await self.llm_improve_prompts(best_prompts, worst_prompts)
            new_prompts.extend(llm_improved)
            print(f"✅ [Optimizer] Generated {len(llm_improved)} LLM-improved prompts")
        except Exception as e:
            print(f"❌ [Optimizer] LLM improvement failed: {e}")
        
        # Method 2: Pattern-based generation (30% of new prompts)
        print(f"\n🔍 [Optimizer] Method 2: Pattern-based generation")
        pattern_based = self.pattern_based_generation(best_prompts)
        new_prompts.extend(pattern_based)
        print(f"✅ [Optimizer] Generated {len(pattern_based)} pattern-based prompts")
        
        # Method 3: Systematic variations (20% of new prompts)
        print(f"\n⚙️ [Optimizer] Method 3: Systematic variations")
        systematic = self.create_systematic_variations(best_prompts[0] if best_prompts else "")
        new_prompts.extend(systematic)
        print(f"✅ [Optimizer] Generated {len(systematic)} systematic variations")
        
        self.generation += 1
        
        print(f"\n🎯 [Optimizer] Evolution complete! Generated {len(new_prompts)} new prompts")
        return new_prompts
    
    async def llm_improve_prompts(self, best_prompts: List[str], worst_prompts: List[str]) -> List[str]:
        """Use Claude to analyze and improve prompts"""
        print(f"🧠 [Optimizer] Analyzing {len(best_prompts)} best and {len(worst_prompts)} worst prompts")
        
        improvement_prompt = f"""You are a prompt engineering expert. Analyze these prompt performance results:

HIGH PERFORMING PROMPTS (use as positive examples):
{chr(10).join(f'{i+1}. "{p[:100]}..."' for i, p in enumerate(best_prompts[:3]))}

LOW PERFORMING PROMPTS (avoid these patterns):
{chr(10).join(f'{i+1}. "{p[:100]}..."' for i, p in enumerate(worst_prompts[:2]))}

Based on this analysis:
1. Identify what makes the high-performing prompts successful
2. Generate exactly 3 NEW improved prompt variations that:
   - Keep successful elements from high performers
   - Avoid patterns from low performers  
   - Add new effective techniques for clear, helpful responses
   - Are concise but comprehensive
   - Use different styles (analytical, creative, balanced)

Return ONLY the 3 new prompts, one per line, no numbering or extra text."""

        print(f"📤 [Optimizer] Sending analysis request to Claude...")
        
        response = await self._get_llm_response(improvement_prompt)
        improved_prompts = [p.strip().strip('"') for p in response.strip().split('\n') if p.strip()]
        
        print(f"📨 [Optimizer] Received {len(improved_prompts)} improved prompts from Claude")
        for i, prompt in enumerate(improved_prompts[:2]):  # Show first 2
            print(f"  💡 [Optimizer] Sample {i+1}: \"{prompt[:60]}...\"")
            
        return improved_prompts[:3]  # Ensure exactly 3 prompts
    
    def pattern_based_generation(self, best_prompts: List[str]) -> List[str]:
        """Generate new prompts based on successful patterns"""
        print(f"🔍 [Optimizer] Extracting patterns from {len(best_prompts)} successful prompts")
        
        # Extract patterns from successful prompts
        patterns = {
            'roles': [],
            'styles': [],
            'structures': [],
            'techniques': []
        }
        
        for prompt in best_prompts:
            patterns['roles'].extend(self._extract_roles(prompt))
            patterns['styles'].extend(self._extract_styles(prompt))
            patterns['structures'].extend(self._extract_structures(prompt))
            patterns['techniques'].extend(self._extract_techniques(prompt))
        
        # Count and rank patterns
        for category in patterns:
            pattern_counts = {}
            for pattern in patterns[category]:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            # Keep most frequent patterns
            patterns[category] = [p for p, count in 
                                sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:3]]
            
            print(f"  🏷️ [Optimizer] Top {category}: {patterns[category]}")
        
        # Generate new prompts using successful patterns
        new_prompts = []
        templates = [
            "You are a {role} AI that provides {style} responses with {structure}. Always {technique}.",
            "Act as a {role} who {style} and uses {structure} format. {technique} in your responses.",
            "You are a {role} assistant. Write in a {style} manner using {structure}. Remember to {technique}."
        ]
        
        for template in templates:
            try:
                new_prompt = template.format(
                    role=random.choice(patterns['roles']) if patterns['roles'] else 'helpful',
                    style=random.choice(patterns['styles']) if patterns['styles'] else 'clear',
                    structure=random.choice(patterns['structures']) if patterns['structures'] else 'organized',
                    technique=random.choice(patterns['techniques']) if patterns['techniques'] else 'be concise'
                )
                new_prompts.append(new_prompt)
                print(f"  ⚡ [Optimizer] Generated: \"{new_prompt[:50]}...\"")
            except Exception as e:
                print(f"  ⚠️ [Optimizer] Template generation failed: {e}")
        
        return new_prompts
    
    def create_systematic_variations(self, best_prompt: str) -> List[str]:
        """Create systematic variations of the best performing prompt"""
        if not best_prompt:
            return []
            
        print(f"⚙️ [Optimizer] Creating systematic variations of best prompt")
        print(f"  🎯 [Optimizer] Base prompt: \"{best_prompt[:50]}...\"")
        
        variations = []
        
        # Variation 1: Add specificity
        specific_variant = best_prompt.replace(
            "You are", "You are an expert"
        ).replace(
            "AI", "AI assistant with deep knowledge"
        )
        variations.append(specific_variant)
        print(f"  🔬 [Optimizer] Specificity variant: \"{specific_variant[:50]}...\"")
        
        # Variation 2: Add structure emphasis
        structure_variant = best_prompt + " Always organize your response clearly with main points."
        variations.append(structure_variant)
        print(f"  📋 [Optimizer] Structure variant: \"{structure_variant[:50]}...\"")
        
        # Variation 3: Add engagement element
        engagement_variant = best_prompt + " Make your explanations engaging and easy to understand."
        variations.append(engagement_variant)
        print(f"  🎪 [Optimizer] Engagement variant: \"{engagement_variant[:50]}...\"")
        
        return variations
    
    def _extract_roles(self, prompt: str) -> List[str]:
        """Extract role patterns from prompt"""
        roles = []
        role_patterns = [
            r'You are (?:a |an )?(\w+(?:\s+\w+)*)',
            r'Act as (?:a |an )?(\w+(?:\s+\w+)*)',
            r'(?:a |an )?(\w+) (?:AI|assistant)'
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, prompt.lower())
            roles.extend(matches)
        
        return [role for role in roles if len(role.split()) <= 3]  # Keep reasonable length
    
    def _extract_styles(self, prompt: str) -> List[str]:
        """Extract style patterns from prompt"""
        style_keywords = [
            'concise', 'detailed', 'engaging', 'analytical', 'creative', 'balanced',
            'clear', 'structured', 'friendly', 'professional', 'enthusiastic',
            'thoughtful', 'direct', 'comprehensive', 'accessible'
        ]
        
        found_styles = []
        for keyword in style_keywords:
            if keyword in prompt.lower():
                found_styles.append(keyword)
        
        return found_styles
    
    def _extract_structures(self, prompt: str) -> List[str]:
        """Extract structural patterns from prompt"""
        structure_keywords = [
            'numbered lists', 'bullet points', 'step by step', 'organized',
            'structured', 'clear format', 'examples', 'pros and cons'
        ]
        
        found_structures = []
        for keyword in structure_keywords:
            if keyword in prompt.lower():
                found_structures.append(keyword)
        
        return found_structures
    
    def _extract_techniques(self, prompt: str) -> List[str]:
        """Extract technique patterns from prompt"""
        technique_patterns = [
            'use examples', 'provide context', 'be specific', 'explain clearly',
            'give reasons', 'show evidence', 'compare options', 'summarize'
        ]
        
        found_techniques = []
        for technique in technique_patterns:
            if technique in prompt.lower():
                found_techniques.append(technique)
        
        return found_techniques
    
    async def _get_llm_response(self, prompt: str) -> str:
        """Helper method to get response from Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ [Optimizer] LLM request failed: {e}")
            return ""
    
    def get_evolution_summary(self) -> Dict:
        """Get summary of evolution progress"""
        if not self.evolution_history:
            return {}
            
        summary = {
            'total_generations': len(self.evolution_history),
            'best_overall_score': max([max([r[1] for r in gen['results']]) 
                                     for gen in self.evolution_history]),
            'improvement_trend': [],
            'successful_patterns': self.successful_patterns
        }
        
        # Calculate improvement trend
        for gen in self.evolution_history:
            avg_score = sum([r[1] for r in gen['results']]) / len(gen['results'])
            best_score = max([r[1] for r in gen['results']])
            summary['improvement_trend'].append({
                'generation': gen['generation'],
                'average_score': avg_score,
                'best_score': best_score
            })
        
        return summary


def calculate_advanced_reward(response: str, query: str, system_prompt: str = "") -> float:
    """Advanced reward calculation based on response quality indicators"""
    print(f"\n🏅 [Reward] Calculating advanced reward for response ({len(response)} chars)")
    
    reward = 0.0
    breakdown = {}
    
    # 1. Length reward (capped at 0.2)
    length_reward = min(len(response) / 500, 1.0) * 0.2
    reward += length_reward
    breakdown['length'] = length_reward
    print(f"  📏 [Reward] Length reward: {length_reward:.3f}")
    
    # 2. Clear structure reward (0.3)
    structure_reward = 0.0
    if has_clear_structure(response):
        structure_reward = 0.3
        reward += structure_reward
    breakdown['structure'] = structure_reward
    print(f"  📋 [Reward] Structure reward: {structure_reward:.3f}")
    
    # 3. Examples usage reward (0.2)
    examples_reward = 0.0
    if uses_examples(response):
        examples_reward = 0.2
        reward += examples_reward
    breakdown['examples'] = examples_reward
    print(f"  💡 [Reward] Examples reward: {examples_reward:.3f}")
    
    # 4. Direct answer reward (0.4)
    directness_reward = 0.0
    if answers_question_directly(response, query):
        directness_reward = 0.4
        reward += directness_reward
    breakdown['directness'] = directness_reward
    print(f"  🎯 [Reward] Directness reward: {directness_reward:.3f}")
    
    # 5. Good conclusion reward (0.1)
    conclusion_reward = 0.0
    if has_good_conclusion(response):
        conclusion_reward = 0.1
        reward += conclusion_reward
    breakdown['conclusion'] = conclusion_reward
    print(f"  🏁 [Reward] Conclusion reward: {conclusion_reward:.3f}")
    
    # Penalties
    penalties = 0.0
    
    # Repetition penalty (-0.2)
    if is_repetitive(response):
        penalties += 0.2
        print(f"  ❌ [Reward] Repetition penalty: -0.2")
    
    # Off-topic penalty (-0.3)
    if is_off_topic(response, query):
        penalties += 0.3
        print(f"  ❌ [Reward] Off-topic penalty: -0.3")
    
    # Empty response penalty (-0.5)
    if not response.strip():
        penalties += 0.5
        print(f"  ❌ [Reward] Empty response penalty: -0.5")
    
    breakdown['penalties'] = -penalties
    reward = max(0.0, reward - penalties)  # Ensure non-negative
    
    print(f"  🎊 [Reward] Final reward: {reward:.3f} (breakdown: {breakdown})")
    return reward


# Quality check functions
def has_clear_structure(response: str) -> bool:
    """Check if response has clear structure"""
    indicators = [
        len(re.findall(r'\n\d+\.', response)) >= 2,  # Numbered lists
        len(re.findall(r'\n[\-\*]', response)) >= 2,  # Bullet points  
        len(re.findall(r'\n\n', response)) >= 2,      # Clear paragraphs
        any(word in response.lower() for word in ['first', 'second', 'finally', 'conclusion'])
    ]
    return sum(indicators) >= 1

def uses_examples(response: str) -> bool:
    """Check if response uses examples"""
    example_indicators = [
        'example' in response.lower(),
        'for instance' in response.lower(), 
        'such as' in response.lower(),
        'like' in response.lower() and len(response) > 100,
        len(re.findall(r'\(.*\)', response)) >= 1  # Parenthetical examples
    ]
    return sum(example_indicators) >= 1

def answers_question_directly(response: str, query: str) -> bool:
    """Check if response directly addresses the query"""
    if not query or not response:
        return False
    
    # Extract key words from query
    query_words = set(re.findall(r'\b\w+\b', query.lower()))
    response_words = set(re.findall(r'\b\w+\b', response.lower()))
    
    # Check overlap
    common_words = query_words.intersection(response_words)
    overlap_ratio = len(common_words) / len(query_words) if query_words else 0
    
    return overlap_ratio >= 0.3  # At least 30% word overlap

def has_good_conclusion(response: str) -> bool:
    """Check if response has a good conclusion"""
    conclusion_indicators = [
        any(word in response.lower()[-200:] for word in 
            ['conclusion', 'summary', 'overall', 'in summary', 'finally', 'therefore']),
        response.strip().endswith('.') and len(response) > 50,
        len(response.split('\n\n')) >= 2  # Multiple paragraphs suggest structure
    ]
    return sum(conclusion_indicators) >= 1

def is_repetitive(response: str) -> bool:
    """Check if response is repetitive"""
    sentences = re.split(r'[.!?]+', response)
    if len(sentences) < 3:
        return False
    
    # Check for repeated sentences or phrases
    sentence_counts = {}
    for sentence in sentences:
        clean_sentence = sentence.strip().lower()
        if len(clean_sentence) > 20:  # Only check substantial sentences
            sentence_counts[clean_sentence] = sentence_counts.get(clean_sentence, 0) + 1
    
    # If any sentence appears more than once, it's repetitive
    return any(count > 1 for count in sentence_counts.values())

def is_off_topic(response: str, query: str) -> bool:
    """Check if response is off-topic (simple heuristic)"""
    if not query or not response:
        return True
    
    # Very basic off-topic detection
    if len(response) < 20:
        return True
    
    # If response doesn't contain any words from query, might be off-topic
    query_words = set(re.findall(r'\b\w{4,}\b', query.lower()))  # Words with 4+ chars
    response_words = set(re.findall(r'\b\w{4,}\b', response.lower()))
    
    if not query_words:
        return False
    
    overlap = len(query_words.intersection(response_words)) / len(query_words)
    return overlap < 0.1  # Less than 10% overlap suggests off-topic