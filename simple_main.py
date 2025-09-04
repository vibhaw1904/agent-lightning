import asyncio
from agentlightning.server import AgentLightningServer
from agentlightning.types import NamedResources, PromptTemplate
from simple_optimizer import SimplePromptOptimizer

async def simple_evolution():
    """Simple 3-step evolution process that's easy to follow"""
    
    print("🌟 SIMPLE PROMPT EVOLUTION DEMO")
    print("=" * 50)
    
    # Step 1: Setup
    print("\n📋 STEP 1: Setup")
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    optimizer = SimplePromptOptimizer()
    await server.start()
    print("✅ Server started")
    
    # Step 2: Start with 3 prompts (good, bad, medium)
    print("\n📋 STEP 2: Initial Prompts (designed to get different scores)")
    prompts = [
        "You are a helpful AI assistant. Provide detailed, well-structured answers with examples and clear explanations.",  # GOOD - should score high
        "Just answer.",  # BAD - too short, vague, should score low
        "You give answers."  # MEDIUM - basic but not terrible
    ]
    
    test_question = "What is artificial intelligence?"
    
    print(f"Testing question: '{test_question}'")
    print(f"Number of prompts to test: {len(prompts)}")
    
    for i, prompt in enumerate(prompts):
        expected = ["HIGH", "LOW", "MEDIUM"][i]
        print(f"  {i+1}. '{prompt}' (Expected: {expected} score)")
    
    # Step 3: Test each prompt and collect scores
    print(f"\n📋 STEP 3: Testing Prompts")
    results = []
    
    for i, prompt in enumerate(prompts):
        print(f"\n🔬 Testing Prompt {i+1}: '{prompt}'")
        
        # Send prompt to client
        resources = {"system_prompt": PromptTemplate(template=prompt, engine="f-string")}
        await server.update_resources(resources)
        
        # Ask the question
        task_id = await server.queue_task(sample={"prompt": test_question}, mode="train")
        print(f"   📤 Sent question to client...")
        
        # Get result
        rollout = await server.poll_completed_rollout(task_id, timeout=15)
        
        if rollout:
            score = rollout.final_reward
            print(f"   ✅ Got response with score: {score:.2f}")
            results.append((prompt, score))
        else:
            print(f"   ❌ No response (timeout)")
            results.append((prompt, 0.0))
    
    # Step 4: Find best and worst
    print(f"\n📋 STEP 4: Results Analysis")
    results.sort(key=lambda x: x[1], reverse=True)  # Sort by score, highest first
    
    best_prompt, best_score = results[0]
    worst_prompt, worst_score = results[-1]
    
    print(f"🏆 BEST:  '{best_prompt}' (Score: {best_score:.2f})")
    print(f"📉 WORST: '{worst_prompt}' (Score: {worst_score:.2f})")
    
    # Step 5: Evolve new prompts
    print(f"\n📋 STEP 5: Evolution")
    
    if best_score > worst_score:
        print("🧬 Creating improved prompts...")
        new_prompts = await optimizer.improve_prompt(best_prompt, worst_prompt, best_score, worst_score)
        
        print(f"\n✨ NEW EVOLVED PROMPTS:")
        for i, prompt in enumerate(new_prompts):
            print(f"  {i+1}. '{prompt}'")
    else:
        print("⚠️  All prompts performed similarly, no evolution needed")
        new_prompts = []
    
    # Step 6: Test evolved prompts (optional)
    if new_prompts:
        print(f"\n📋 STEP 6: Testing Evolved Prompts")
        
        for i, prompt in enumerate(new_prompts):
            print(f"\n🧪 Testing Evolved Prompt {i+1}: '{prompt[:30]}...'")
            
            resources = {"system_prompt": PromptTemplate(template=prompt, engine="f-string")}
            await server.update_resources(resources)
            
            task_id = await server.queue_task(sample={"prompt": test_question}, mode="train")
            rollout = await server.poll_completed_rollout(task_id, timeout=15)
            
            if rollout:
                score = rollout.final_reward
                print(f"   ✅ Evolved prompt scored: {score:.2f}")
                
                if score > best_score:
                    print(f"   🎉 IMPROVEMENT! New best score: {score:.2f} (was {best_score:.2f})")
                else:
                    print(f"   📊 No improvement (best was still {best_score:.2f})")
            else:
                print(f"   ❌ No response")
    
    # Cleanup
    print(f"\n📋 STEP 7: Cleanup")
    await server.stop()
    print("✅ Demo complete!")
    
    return results, new_prompts

if __name__ == "__main__":
    print("🚀 Make sure 'python run_client.py' is running in another terminal!")
    input("Press Enter when ready...")
    
    results, evolved = asyncio.run(simple_evolution())
    
    print(f"\n🎊 SUMMARY:")
    print(f"   Tested: {len(results)} original prompts")
    print(f"   Evolved: {len(evolved)} new prompts") 
    print(f"   Best score: {max(r[1] for r in results):.2f}")
    print("=" * 50)