import anthropic
import os
import json
import asyncio

class AdvancedPromptOptimizer:
    """Advanced prompt optimizer using LLM-as-a-Judge for sophisticated reward calculation"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    async def evolve_prompts(self, best_prompt, worst_prompt, best_score, worst_score):
        """Create evolved prompts using advanced analysis"""
        
        evolution_request = f"""You are an expert in AI prompt engineering. Analyze these test results:

BEST PROMPT (Score: {best_score:.2f}):
"{best_prompt}"

WORST PROMPT (Score: {worst_score:.2f}):
"{worst_prompt}"

The scoring considers: accuracy, clarity, completeness, helpfulness, and structure.

Create exactly 2 improved prompts that:
1. Combine the most effective elements from the best prompt
2. Address the weaknesses found in the worst prompt
3. Add specific improvements for better AI responses
4. Maintain clarity while adding sophistication

Return only the 2 prompts, one per line."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Using correct model name
            max_tokens=500,
            messages=[{"role": "user", "content": evolution_request}]
        )
        
        evolved_prompts = [
            line.strip().strip('"') 
            for line in response.content[0].text.strip().split('\n') 
            if line.strip() and len(line.strip()) > 30
        ]
        
        return evolved_prompts[:2]


class LLMJudge:
    """LLM-as-a-Judge system for advanced response evaluation"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    async def evaluate_response(self, question, response, system_prompt=""):
        """Comprehensive evaluation using Claude as a judge"""
        
        evaluation_prompt = f"""You are an expert evaluator of AI responses. Please evaluate this response comprehensively.

ORIGINAL QUESTION:
"{question}"

AI RESPONSE TO EVALUATE:
"{response}"

SYSTEM PROMPT USED:
"{system_prompt}"

Please evaluate the response on these 5 dimensions, each scored 0-20 points:

1. ACCURACY (0-20): Is the information factually correct and reliable?
2. CLARITY (0-20): Is the response clear, well-written, and easy to understand?
3. COMPLETENESS (0-20): Does it fully address all parts of the question?
4. HELPFULNESS (0-20): Is it practically useful and actionable for the user?
5. STRUCTURE (0-20): Is it well-organized with good flow and formatting?

For each dimension:
- Give a score (0-20)
- Provide a brief 1-2 sentence explanation

Then provide:
- TOTAL SCORE (sum of all dimensions, 0-100)
- OVERALL ASSESSMENT (2-3 sentences on the response quality)

Format your response as JSON:
{{
    "accuracy": {{"score": X, "explanation": "..."}},
    "clarity": {{"score": X, "explanation": "..."}},
    "completeness": {{"score": X, "explanation": "..."}},
    "helpfulness": {{"score": X, "explanation": "..."}},
    "structure": {{"score": X, "explanation": "..."}},
    "total_score": X,
    "overall_assessment": "..."
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Using correct model name
                max_tokens=800,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )
            
            # Parse JSON response
            evaluation_text = response.content[0].text.strip()
            
            # Extract JSON from response (handles cases where Claude adds extra text)
            start_idx = evaluation_text.find('{')
            end_idx = evaluation_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_text = evaluation_text[start_idx:end_idx]
                evaluation = json.loads(json_text)
                
                # Convert to 0-1 scale for compatibility
                final_score = evaluation["total_score"] / 100.0
                
                return {
                    "score": final_score,
                    "detailed_evaluation": evaluation
                }
            else:
                # Fallback if JSON parsing fails
                return {"score": 0.5, "detailed_evaluation": {"error": "Failed to parse evaluation"}}
                
        except Exception as e:
            print(f"🔴 Evaluation error: {e}")
            return {"score": 0.0, "detailed_evaluation": {"error": str(e)}}


class CompariativeJudge:
    """LLM judge that compares two responses directly"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    async def compare_responses(self, question, response_a, response_b, prompt_a="", prompt_b=""):
        """Compare two responses and determine which is better"""
        
        comparison_prompt = f"""You are an expert evaluator. Compare these two AI responses to the same question.

QUESTION:
"{question}"

RESPONSE A (Prompt: "{prompt_a[:50]}..."):
"{response_a}"

RESPONSE B (Prompt: "{prompt_b[:50]}..."):  
"{response_b}"

Please compare them on:
1. Accuracy of information
2. Clarity and readability
3. Completeness of answer
4. Practical helpfulness
5. Organization and structure

Provide your evaluation in JSON format:
{{
    "winner": "A" or "B" or "TIE",
    "confidence": 0.1-1.0,
    "reasoning": "Detailed explanation of why one is better",
    "scores": {{
        "response_a": 0.0-1.0,
        "response_b": 0.0-1.0
    }}
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": comparison_prompt}]
            )
            
            # Parse JSON response
            eval_text = response.content[0].text.strip()
            start_idx = eval_text.find('{')
            end_idx = eval_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_text = eval_text[start_idx:end_idx]
                comparison = json.loads(json_text)
                return comparison
            else:
                return {"winner": "TIE", "confidence": 0.5, "reasoning": "Parse error", "scores": {"response_a": 0.5, "response_b": 0.5}}
                
        except Exception as e:
            print(f"🔴 Comparison error: {e}")
            return {"winner": "TIE", "confidence": 0.5, "reasoning": str(e), "scores": {"response_a": 0.5, "response_b": 0.5}}


# Main evaluation function to use in run_client.py
async def calculate_advanced_reward(response, question, system_prompt="", method="individual"):
    """
    Advanced reward calculation using LLM-as-a-Judge
    
    Args:
        response: The AI response to evaluate
        question: The original question
        system_prompt: The system prompt used
        method: "individual" for single evaluation, "comparative" for head-to-head comparison
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    
    if method == "individual":
        judge = LLMJudge()
        evaluation = await judge.evaluate_response(question, response, system_prompt)
        
        # Print detailed breakdown for visibility
        if "detailed_evaluation" in evaluation and "error" not in evaluation["detailed_evaluation"]:
            details = evaluation["detailed_evaluation"]
            print(f"\n📊 LLM Judge Evaluation:")
            print(f"   🎯 Accuracy: {details['accuracy']['score']}/20 - {details['accuracy']['explanation']}")
            print(f"   💡 Clarity: {details['clarity']['score']}/20 - {details['clarity']['explanation']}")  
            print(f"   ✅ Completeness: {details['completeness']['score']}/20 - {details['completeness']['explanation']}")
            print(f"   🤝 Helpfulness: {details['helpfulness']['score']}/20 - {details['helpfulness']['explanation']}")
            print(f"   📋 Structure: {details['structure']['score']}/20 - {details['structure']['explanation']}")
            print(f"   🏆 Total: {details['total_score']}/100 ({evaluation['score']:.2f})")
            print(f"   💬 Assessment: {details['overall_assessment']}")
        
        return evaluation["score"]
    
    else:
        # For comparative method, you'd need to store previous responses to compare against
        # This is more complex and would require modifications to the main flow
        judge = LLMJudge()
        evaluation = await judge.evaluate_response(question, response, system_prompt)
        return evaluation["score"]


# Simplified version for easier integration
async def simple_llm_judge_reward(response, question):
    """Simplified LLM judge for easy integration"""
    
    judge_prompt = f"""Rate this AI response on a scale of 0-100:

QUESTION: "{question}"
RESPONSE: "{response}"

Consider:
- Accuracy and correctness
- Clarity and readability  
- Completeness of answer
- Helpfulness to user
- Good organization

Respond with just the number (0-100):"""

    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Faster model for simple scoring
            max_tokens=50,
            messages=[{"role": "user", "content": judge_prompt}]
        )
        
        # Extract number from response
        score_text = response.content[0].text.strip()
        score = float(score_text) / 100.0  # Convert to 0-1 scale
        
        return max(0.0, min(1.0, score))  # Ensure within bounds
        
    except Exception as e:
        print(f"🔴 Simple judge error: {e}")
        return 0.5  # Default score on error