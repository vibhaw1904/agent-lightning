import anthropic
import os
import re

class SimplePromptOptimizer:
    """Simple prompt optimizer that's easy to understand"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        print("✨ Simple Optimizer initialized")
    
    async def improve_prompt(self, best_prompt, worst_prompt, best_score, worst_score):
        """Take the best and worst prompt, create 2 improved versions"""
        print(f"\n🔬 Analyzing prompts...")
        print(f"   🏆 Best: '{best_prompt[:100]}...' (Score: {best_score:.2f})")
        print(f"   📉 Worst: '{worst_prompt[:100]}...' (Score: {worst_score:.2f})")
        
        improvement_request = f"""I tested these 2 prompts:

BEST PERFORMING (Score: {best_score:.2f}):
"{best_prompt}"

WORST PERFORMING (Score: {worst_score:.2f}):
"{worst_prompt}"

Create exactly 2 improved prompts that:
1. Keep what worked in the best prompt
2. Avoid what didn't work in the worst prompt
3. Add one new helpful element

Return only the 2 new prompts, one per line."""

        print("🤖 Asking Claude to improve prompts...")
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": improvement_request}]
        )
        
        improved_prompts = [line.strip().strip('"') for line in response.content[0].text.strip().split('\n') if line.strip()]
        
        print(f"✅ Generated {len(improved_prompts)} improved prompts:")
        for i, prompt in enumerate(improved_prompts[:2]):
            print(f"   {i+1}. '{prompt[:40]}...'")
            
        return improved_prompts[:2]  # Return exactly 2 prompts


def calculate_simple_reward(response, question):
    """Simple reward calculation that's easy to understand"""
    print(f"\n📊 Calculating reward for {len(response)} character response")
    
    reward = 0.0
    
    # 1. Length check (30% of score) - More strict to show differences
    if 100 <= len(response) <= 400:
        length_score = 0.3
        print(f"   ✅ Good length ({len(response)} chars): +0.3")
    elif 50 <= len(response) <= 600:
        length_score = 0.15
        print(f"   ⚠️  Okay length ({len(response)} chars): +0.15")
    else:
        length_score = 0.0
        print(f"   ❌ Bad length ({len(response)} chars): +0.0")
    reward += length_score
    
    # 2. Structure check (30% of score) - More detailed
    sentence_count = len(re.findall(r'[.!?]+', response))
    paragraph_count = len(response.split('\n\n'))
    
    if sentence_count >= 3 and (paragraph_count >= 2 or '\n' in response):
        structure_score = 0.3
        print(f"   ✅ Great structure ({sentence_count} sentences, paragraphs): +0.3")
    elif sentence_count >= 2:
        structure_score = 0.15  
        print(f"   ⚠️  Basic structure ({sentence_count} sentences): +0.15")
    else:
        structure_score = 0.0
        print(f"   ❌ Poor structure ({sentence_count} sentences): +0.0")
    reward += structure_score
    
    # 3. Relevance check (40% of score) - More nuanced
    question_words = set(question.lower().split())
    response_words = set(response.lower().split())
    common_words = len(question_words.intersection(response_words))
    overlap_ratio = common_words / len(question_words) if question_words else 0
    
    if overlap_ratio >= 0.5 and common_words >= 3:
        relevance_score = 0.4
        print(f"   ✅ Highly relevant ({common_words} matching words, {overlap_ratio:.1%} overlap): +0.4")
    elif overlap_ratio >= 0.3 or common_words >= 2:
        relevance_score = 0.2
        print(f"   ⚠️  Somewhat relevant ({common_words} matching words, {overlap_ratio:.1%} overlap): +0.2")
    else:
        relevance_score = 0.0
        print(f"   ❌ Not relevant ({common_words} matching words, {overlap_ratio:.1%} overlap): +0.0")
    reward += relevance_score
    
    print(f"   🎯 Total reward: {reward:.2f}")
    return reward