import anthropic
import os
import re

class PromptOptimizer:
    """Clean prompt optimizer focused on evolution"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    async def evolve_prompts(self, best_prompt, worst_prompt, best_score, worst_score):
        """Create 2 evolved prompts from best/worst analysis"""
        
        evolution_request = f"""I'm optimizing AI prompts. Here are my test results:

BEST PROMPT (Score: {best_score:.2f}):
"{best_prompt}"

WORST PROMPT (Score: {worst_score:.2f}):
"{worst_prompt}"

The scoring system rewards:
- Good length (100-400 chars): up to 30 points
- Clear structure (multiple sentences/paragraphs): up to 30 points  
- Relevance (matches question keywords): up to 40 points

Create exactly 2 improved prompts that:
1. Keep successful elements from the best prompt
2. Avoid problems from the worst prompt
3. Add specific improvements for better structure and detail

Return only the 2 prompts, one per line, no extra text."""

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            messages=[{"role": "user", "content": evolution_request}]
        )
        
        evolved_prompts = [
            line.strip().strip('"') 
            for line in response.content[0].text.strip().split('\n') 
            if line.strip() and len(line.strip()) > 20
        ]
        
        return evolved_prompts[:2]  # Return exactly 2


def calculate_reward(response, question):
    """Clean reward calculation with 3 components"""
    
    reward = 0.0
    
    # 1. Length (30% max)
    length = len(response)
    if 100 <= length <= 400:
        length_score = 0.30
    elif 50 <= length <= 600:
        length_score = 0.15
    else:
        length_score = 0.00
    reward += length_score
    
    # 2. Structure (30% max)
    sentences = len(re.findall(r'[.!?]+', response))
    has_paragraphs = '\n' in response or len(response.split('. ')) >= 3
    
    if sentences >= 3 and has_paragraphs:
        structure_score = 0.30
    elif sentences >= 2:
        structure_score = 0.15
    else:
        structure_score = 0.00
    reward += structure_score
    
    # 3. Relevance (40% max) 
    question_words = set(question.lower().split())
    response_words = set(response.lower().split())
    common_words = len(question_words.intersection(response_words))
    overlap_ratio = common_words / len(question_words) if question_words else 0
    
    if overlap_ratio >= 0.5 and common_words >= 3:
        relevance_score = 0.40
    elif overlap_ratio >= 0.3 or common_words >= 2:
        relevance_score = 0.20
    else:
        relevance_score = 0.00
    reward += relevance_score
    
    return reward