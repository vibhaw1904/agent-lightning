# Prompt Evolution Flow - Step by Step

## 🎯 Overview
This system automatically evolves better AI prompts by testing different prompt styles, finding what works best, and creating improved versions using AI analysis.

## 📁 File Structure

### `main.py` - Evolution Controller
- Manages the entire evolution process
- Tests 5 different prompt styles  
- Coordinates between server and optimizer
- Shows clear results and improvements

### `run_client.py` - AI Worker
- Receives prompts and questions from main.py
- Uses Claude AI to generate responses
- Calculates quality scores for each response
- Returns scores back to main.py

### `prompt_optimizer.py` - Evolution Engine
- Analyzes best vs worst performing prompts
- Uses Claude AI to create improved prompt versions
- Contains the reward calculation system
- Returns 2 evolved prompts

## 🔄 Complete Flow

### Step 1: System Setup
```
🧬 PROMPT EVOLUTION SYSTEM
✅ System ready
```
**What happens:**
- Starts Agent Lightning server on port 9997
- Initializes the PromptOptimizer class
- Waits for client connection

### Step 2: Initial Prompt Testing
```
📝 Testing 5 prompts  
🎯 Question: 'Explain how machine learning algorithms learn from data...'

🔬 Testing Prompt 1/5
   Score: 0.85

🔬 Testing Prompt 2/5  
   Score: 0.15

🔬 Testing Prompt 3/5
   Score: 0.70

🔬 Testing Prompt 4/5
   Score: 0.25

🔬 Testing Prompt 5/5
   Score: 0.50
```

**What happens:**
1. **main.py** sends each prompt + question to **run_client.py**
2. **run_client.py** uses Claude to generate an answer with that prompt
3. **run_client.py** calculates a score (0.0-1.0) based on:
   - Length (30%): Is the response 100-400 characters?
   - Structure (30%): Does it have multiple sentences/paragraphs?  
   - Relevance (40%): Does it use words from the original question?
4. **main.py** receives the score back

### Step 3: Results Analysis
```
📊 RESULTS:
   1. 0.85 - You are an expert AI assistant with deep knowledge...
   2. 0.70 - You are a helpful AI assistant that provides clear...
   3. 0.50 - You are an AI that answers questions with reasonable...
   4. 0.25 - You respond to questions. Try to be helpful sometimes...
   5. 0.15 - Answer the question. Keep it short.

🏆 Best: 0.85
📉 Worst: 0.15
```

**What happens:**
- All results are sorted from highest to lowest score
- Best and worst prompts are identified
- Clear performance differences are shown

### Step 4: Evolution Process
```
🧬 EVOLUTION
✅ Created 2 evolved prompts
```

**What happens inside `prompt_optimizer.py`:**

1. **Analysis Phase:**
   ```python
   evolution_request = f"""I'm optimizing AI prompts. Here are my test results:

   BEST PROMPT (Score: 0.85):
   "You are an expert AI assistant with deep knowledge..."

   WORST PROMPT (Score: 0.15):  
   "Answer the question. Keep it short."

   The scoring system rewards:
   - Good length (100-400 chars): up to 30 points
   - Clear structure: up to 30 points
   - Relevance: up to 40 points

   Create exactly 2 improved prompts that:
   1. Keep successful elements from the best prompt
   2. Avoid problems from the worst prompt  
   3. Add specific improvements for better structure and detail
   ```

2. **Claude Analysis:**
   - Claude analyzes what made the best prompt successful
   - Claude identifies what made the worst prompt fail
   - Claude creates 2 new improved prompt versions

3. **Return Results:**
   - 2 new evolved prompts are returned to main.py

### Step 5: Testing Evolved Prompts
```
🧪 Testing evolved prompts
   Evolved 1: 0.90
   Evolved 2: 0.88

🎉 IMPROVEMENT: +0.05 (+5.9%)
```

**What happens:**
- Each evolved prompt is tested with the same question
- Scores are compared to the original best score
- Improvement percentage is calculated and shown

## 📊 Reward System Breakdown

### `calculate_reward(response, question)` Function

**Input:** AI response text + original question
**Output:** Score from 0.0 to 1.0

#### Component 1: Length Score (30% of total)
```python
length = len(response)
if 100 <= length <= 400:    # Perfect range
    length_score = 0.30
elif 50 <= length <= 600:   # Acceptable range  
    length_score = 0.15
else:                        # Too short or too long
    length_score = 0.00
```

#### Component 2: Structure Score (30% of total)
```python
sentences = len(re.findall(r'[.!?]+', response))
has_paragraphs = '\n' in response or len(response.split('. ')) >= 3

if sentences >= 3 and has_paragraphs:  # Well structured
    structure_score = 0.30
elif sentences >= 2:                   # Basic structure
    structure_score = 0.15  
else:                                  # Poor structure
    structure_score = 0.00
```

#### Component 3: Relevance Score (40% of total)
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
```

## 🧬 Evolution Strategy Explained

### Why This Works:

1. **Quality Measurement:** We can automatically detect response quality
2. **Pattern Recognition:** Claude can identify what makes prompts successful  
3. **Iterative Improvement:** Each evolution builds on previous successes
4. **Objective Testing:** Same question tests all prompts fairly

### Example Evolution:
```
Original Worst: "Answer the question. Keep it short."
Problems: Too vague, encourages brief responses, no guidance

↓ Claude Analysis ↓

Evolved: "You are a knowledgeable AI assistant that provides comprehensive, 
well-structured answers. When responding, include relevant details and 
organize your thoughts clearly to ensure the user gets complete information."

Improvements: Specific role, encourages detail, asks for structure
```

### Evolution Cycle:
```
Test Prompts → Identify Best/Worst → AI Analysis → Generate Improved → Test Again
     ↑                                                                      ↓
     ←←←←←←←←←←← Continue with best evolved prompts ←←←←←←←←←←←←←←←
```

## 🎯 Expected Results

**You should see:**
- Clear score differences between prompts (0.15 to 0.85 range)
- Evolved prompts that score higher than originals
- Obvious quality improvements in the evolved prompts
- Percentage improvements shown clearly

**The system learns:**
- Specific language that produces better responses
- Structural elements that improve clarity
- How to combine successful elements from multiple prompts
- What to avoid from poor-performing prompts

This creates a continuous improvement cycle that automatically evolves better AI prompts!

## 🚀 Running the System

**Terminal 1 (Server):**
```bash
python main.py
```

**Terminal 2 (Client):**
```bash  
python run_client.py
```

**Environment:**
```bash
# In .env file:
ANTHROPIC_API_KEY=your_key_here
```

The system will run once and show you the complete evolution process with clear before/after comparisons!