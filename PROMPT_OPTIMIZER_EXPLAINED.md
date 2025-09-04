# prompt_optimizer.py - Detailed Explanation

## 🎯 What This File Does

`prompt_optimizer.py` is the brain of the evolution system. It takes the best and worst performing prompts, analyzes why they succeeded or failed, and creates improved versions using AI.

## 📋 File Structure

```python
import anthropic  # For Claude AI integration
import os         # For environment variables  
import re         # For text pattern matching

class PromptOptimizer:
    # Main evolution class
    
def calculate_reward(response, question):
    # Scoring function
```

## 🧬 Class: PromptOptimizer

### `__init__(self)`
```python
def __init__(self):
    self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

**Purpose:** Initialize the optimizer with Claude AI access
**What it does:**
- Creates an Anthropic client using your API key
- This client will be used to analyze prompts and create improvements

### `evolve_prompts(self, best_prompt, worst_prompt, best_score, worst_score)`

This is the core evolution function. Let's break it down:

#### Input Parameters:
- `best_prompt`: The highest scoring prompt text
- `worst_prompt`: The lowest scoring prompt text  
- `best_score`: Score of the best prompt (e.g., 0.85)
- `worst_score`: Score of the worst prompt (e.g., 0.15)

#### Step 1: Create Analysis Request
```python
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
```

**What this does:**
- Gives Claude the context of our optimization task
- Shows Claude examples of what worked and what didn't
- Explains our scoring criteria so Claude knows what to optimize for
- Asks for exactly 2 improved prompts with specific instructions

#### Step 2: Send to Claude AI
```python
response = self.client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=400,
    messages=[{"role": "user", "content": evolution_request}]
)
```

**What this does:**
- Sends our analysis request to Claude
- Uses Claude-3-Haiku (fast, cost-effective model)
- Limits response to 400 tokens to keep prompts concise

#### Step 3: Parse Response
```python
evolved_prompts = [
    line.strip().strip('"') 
    for line in response.content[0].text.strip().split('\n') 
    if line.strip() and len(line.strip()) > 20
]

return evolved_prompts[:2]  # Return exactly 2
```

**What this does:**
- Splits Claude's response into separate lines
- Removes whitespace and quote marks
- Filters out empty lines or very short lines
- Returns exactly 2 prompts (ignores extras if Claude provides more)

## 📊 Function: calculate_reward

This function evaluates how good an AI response is using 3 criteria:

### Input:
- `response`: The AI's answer text
- `question`: The original question asked

### Output:
- A score from 0.0 to 1.0 (higher = better)

### Component 1: Length Scoring (30% of total)
```python
length = len(response)
if 100 <= length <= 400:    # Sweet spot
    length_score = 0.30
elif 50 <= length <= 600:   # Acceptable  
    length_score = 0.15
else:                        # Too short or too long
    length_score = 0.00
reward += length_score
```

**Logic:**
- **Perfect range (100-400 chars):** Detailed but not overwhelming → Full points (0.30)
- **Acceptable range (50-600 chars):** Okay but not ideal → Half points (0.15)
- **Outside range:** Too brief or too verbose → No points (0.00)

### Component 2: Structure Scoring (30% of total)
```python
sentences = len(re.findall(r'[.!?]+', response))
has_paragraphs = '\n' in response or len(response.split('. ')) >= 3

if sentences >= 3 and has_paragraphs:  # Well organized
    structure_score = 0.30
elif sentences >= 2:                   # Basic organization
    structure_score = 0.15
else:                                  # Poor organization  
    structure_score = 0.00
reward += structure_score
```

**Logic:**
- **Great structure:** 3+ sentences AND paragraphs/breaks → Full points (0.30)
- **Basic structure:** At least 2 sentences → Half points (0.15)  
- **Poor structure:** Single sentence or fragment → No points (0.00)

**How it detects structure:**
- `re.findall(r'[.!?]+', response)`: Counts sentences by finding punctuation
- `'\n' in response`: Checks for paragraph breaks
- `len(response.split('. ')) >= 3`: Alternative check for sentence breaks

### Component 3: Relevance Scoring (40% of total - Most Important)
```python
question_words = set(question.lower().split())
response_words = set(response.lower().split())
common_words = len(question_words.intersection(response_words))
overlap_ratio = common_words / len(question_words)

if overlap_ratio >= 0.5 and common_words >= 3:  # Highly relevant
    relevance_score = 0.40
elif overlap_ratio >= 0.3 or common_words >= 2:  # Somewhat relevant
    relevance_score = 0.20
else:                                            # Not relevant
    relevance_score = 0.00
reward += relevance_score
```

**Logic:**
- **Highly relevant:** 50%+ word overlap AND 3+ shared words → Full points (0.40)
- **Somewhat relevant:** 30%+ overlap OR 2+ shared words → Half points (0.20)
- **Not relevant:** Low word overlap → No points (0.00)

**Example:**
```python
question = "How does machine learning work?"
response = "Machine learning algorithms work by finding patterns in data..."

question_words = {"how", "does", "machine", "learning", "work"}
response_words = {"machine", "learning", "algorithms", "work", "by", "finding", "patterns", "in", "data"}

common_words = {"machine", "learning", "work"} = 3 words
overlap_ratio = 3/5 = 0.6 (60%)

Result: 0.6 >= 0.5 AND 3 >= 3 → relevance_score = 0.40
```

## 🔄 How Evolution Works - Complete Example

### Initial State:
```python
best_prompt = "You are an expert AI assistant with deep knowledge..."
best_score = 0.85

worst_prompt = "Answer the question. Keep it short."  
worst_score = 0.15
```

### Claude's Analysis Process:
1. **Identifies success patterns:** "expert", "deep knowledge", detailed instructions
2. **Identifies failure patterns:** "keep it short", vague instructions, no guidance
3. **Combines insights:** Keep expertise + depth, avoid brevity commands
4. **Adds improvements:** Better structure guidance, more specific instructions

### Evolution Result:
```python
evolved_prompts = [
    "You are an expert AI assistant with comprehensive knowledge. Provide detailed, well-structured responses that thoroughly address all aspects of the user's question with clear explanations and relevant examples.",
    
    "You are a knowledgeable AI that excels at giving informative answers. Structure your responses clearly with multiple sentences, include specific details, and ensure you directly address what the user is asking about."
]
```

### Why These Are Better:
- **Keeps successful elements:** "expert", "knowledgeable" 
- **Avoids failure patterns:** No "keep it short" commands
- **Adds improvements:** "well-structured", "clear explanations", "multiple sentences"
- **More specific:** "thoroughly address", "relevant examples", "directly address"

## 🎯 Key Design Decisions

### Why 3 Scoring Components?
- **Length:** Ensures responses aren't too brief or verbose
- **Structure:** Rewards clear, organized communication  
- **Relevance:** Most important - ensures responses actually answer the question

### Why Different Weights? (30%, 30%, 40%)
- **Relevance gets 40%:** Most critical - irrelevant answers are useless
- **Length/Structure get 30% each:** Both important for quality but secondary to relevance

### Why Use Claude for Evolution?
- **Pattern Recognition:** Claude can identify subtle patterns in successful prompts
- **Language Generation:** Claude excels at creating coherent, improved prompt text
- **Context Understanding:** Claude understands the goal and can make targeted improvements

This system creates a feedback loop where prompts continuously improve based on measured performance, leading to automatically optimized AI interactions!