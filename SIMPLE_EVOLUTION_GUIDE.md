# Simple Prompt Evolution Guide

## 🎯 What This Does

This system automatically improves AI prompts by:
1. Testing different prompts
2. Finding which ones work best  
3. Creating improved versions
4. Testing the improvements

## 📁 Files Overview

### `simple_main.py` - The Main Process
- Runs the evolution experiment
- Tests 3 simple prompts
- Shows step-by-step what's happening

### `simple_client.py` - The AI Worker  
- Receives prompts from main
- Calls Claude AI to answer questions
- Calculates how good each answer is

### `simple_optimizer.py` - The Improver
- Takes best and worst prompts
- Uses Claude to create better versions
- Simple reward calculation

## 🔄 Step-by-Step Process

### Step 1: Setup
```
🌟 SIMPLE PROMPT EVOLUTION DEMO
📋 STEP 1: Setup
✅ Server started
```
- Starts the Agent Lightning server
- Initializes the optimizer

### Step 2: Initial Prompts
```
📋 STEP 2: Initial Prompts
Testing question: 'What is artificial intelligence?'
Number of prompts to test: 3
  1. 'You are helpful.'
  2. 'You are a detailed AI assistant that provides comprehensive answers.'  
  3. 'You are brief and direct.'
```
- We start with 3 very different prompt styles
- Each will answer the same question
- We'll see which style works best

### Step 3: Testing Each Prompt
```
📋 STEP 3: Testing Prompts
🔬 Testing Prompt 1: 'You are helpful.'
   📤 Sent question to client...
   ✅ Got response with score: 0.60
```

**What happens here:**
1. **Server** sends prompt + question to **Client**
2. **Client** uses the prompt to ask Claude AI
3. **Client** calculates reward based on:
   - **Length** (30%): Is answer 50-500 characters?
   - **Structure** (30%): Does it have sentences/paragraphs?  
   - **Relevance** (40%): Does it answer the question?
4. **Server** gets the score back

### Step 4: Find Best and Worst
```
📋 STEP 4: Results Analysis
🏆 BEST:  'You are a detailed AI assistant...' (Score: 0.90)
📉 WORST: 'You are brief and direct.' (Score: 0.30)
```
- Sorts all prompts by their scores
- Identifies the highest and lowest performers

### Step 5: Evolution 
```
📋 STEP 5: Evolution  
🧬 Creating improved prompts...
🤖 Asking Claude to improve prompts...
✅ Generated 2 improved prompts:
  1. 'You are a helpful and detailed AI assistant who provides clear, comprehensive answers with good structure.'
  2. 'You are an AI that gives thorough responses while being easy to understand and well-organized.'
```

**Evolution Process:**
1. Send best and worst prompts to Claude
2. Ask Claude to analyze what worked and what didn't  
3. Claude creates 2 new improved prompts
4. New prompts keep good parts, fix bad parts, add improvements

### Step 6: Test Improvements
```
📋 STEP 6: Testing Evolved Prompts
🧪 Testing Evolved Prompt 1: 'You are a helpful and detailed...'
   ✅ Evolved prompt scored: 0.95
   🎉 IMPROVEMENT! New best score: 0.95 (was 0.90)
```
- Tests the new evolved prompts
- Compares with original best score
- Shows if evolution actually improved performance

## 🏆 Reward System Explained

### Simple Scoring (0.0 to 1.0):

**Length Check (30% of score):**
- ✅ Good (50-500 chars): +0.3 points
- ❌ Too short/long: +0.0 points

**Structure Check (30% of score):**  
- ✅ Has sentences/paragraphs: +0.3 points
- ❌ Just one blob of text: +0.0 points

**Relevance Check (40% of score):**
- ✅ Uses 2+ words from question: +0.4 points  
- ❌ Doesn't match question: +0.0 points

**Example Scoring:**
```
📊 Calculating reward for 234 character response
   ✅ Good length: +0.3
   ✅ Has structure: +0.3  
   ✅ Relevant (4 matching words): +0.4
   🎯 Total reward: 1.0
```

## 🚀 How to Run

### Terminal 1 (Server):
```bash
python simple_main.py
```

### Terminal 2 (Client):  
```bash
python simple_client.py
```

### Environment Setup:
```bash
# Create .env file with:
ANTHROPIC_API_KEY=your_key_here
```

## 📊 What You'll See

### Console Output Flow:
1. **Setup messages** - System starting up
2. **Prompt testing** - Each prompt being evaluated
3. **Client work** - AI generating responses and scoring them
4. **Evolution** - New prompts being created
5. **Improvement testing** - Seeing if evolution worked
6. **Final summary** - Overall results

### Key Indicators:
- 🏆 = Best performing prompt
- 📉 = Worst performing prompt  
- 🧬 = Evolution happening
- 🎉 = Improvement found!
- ✅ = Success
- ❌ = Problem/failure

## 💡 Understanding the Evolution

### Why This Works:
1. **Different prompts produce different quality responses**
2. **We can measure response quality automatically** 
3. **AI (Claude) can analyze what makes prompts good**
4. **AI can create improved versions based on analysis**
5. **We can test if improvements actually work**

### Example Evolution:
```
Original: "You are helpful."
→ Problem: Too vague, produces short answers

Evolved: "You are a helpful AI assistant who provides clear, well-structured answers with specific details."
→ Better: More specific, encourages structure and detail
```

## 🔄 The Evolution Cycle

```
Test Prompts → Find Best/Worst → Analyze Patterns → Create Improvements → Test Again
     ↑                                                                        ↓
     ←←←←←←←←←←←←←←←← Repeat with new prompts ←←←←←←←←←←←←←←←←←←←←←←
```

This creates a continuous improvement loop where prompts get better over time!

## 🎯 Expected Results

You should see:
- **Different scores** for different prompt styles
- **Evolved prompts** that combine the best elements  
- **Improved scores** for evolved prompts (usually)
- **Clear explanations** of why each score was given

The system learns what makes prompts effective and automatically creates better ones!