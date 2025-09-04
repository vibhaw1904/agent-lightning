import asyncio
from agentlightning.server import AgentLightningServer
from agentlightning.types import NamedResources, PromptTemplate
from prompt_optimizer import PromptOptimizer

async def run_evolution():
    """Clean evolution process with 5 prompts"""
    
    print("🧬 PROMPT EVOLUTION SYSTEM")
    print("=" * 40)
    
    # Setup
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    optimizer = PromptOptimizer()
    await server.start()
    print("✅ System ready")
    
    # 5 prompts with clear quality differences (100+ words each)
    prompts = [
        # EXCELLENT - Should score 0.8-1.0
        "You are an expert AI assistant with deep knowledge across multiple domains. When answering questions, you should provide comprehensive, well-structured responses that include relevant examples, clear explanations, and practical insights. Always organize your thoughts into logical sections, use specific details to support your points, and ensure your response directly addresses all aspects of the user's question. Your goal is to be both informative and accessible, making complex topics understandable while maintaining accuracy and depth.",
        
        # VERY POOR - Should score 0.0-0.2
        "Answer the question. Keep it short.",
        
        # GOOD - Should score 0.6-0.8
        "You are a helpful AI assistant that provides clear and informative responses. When someone asks a question, make sure to give a detailed answer that covers the main points. Use examples when helpful and organize your response in a logical way. Always try to be accurate and comprehensive while keeping your explanation accessible to the user.",
        
        # POOR - Should score 0.2-0.4
        "You respond to questions. Try to be helpful sometimes. Give information when you can.",
        
        # AVERAGE - Should score 0.4-0.6
        "You are an AI that answers questions with reasonable detail. Provide useful information and try to structure your responses clearly. Make sure your answers are relevant to what the user is asking about."
    ]
    
    test_question = "Explain how machine learning algorithms learn from data and improve their performance over time."
    
    print(f"\n📝 Testing {len(prompts)} prompts")
    print(f"🎯 Question: '{test_question}'")
    
    # Test all prompts
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n🔬 Testing Prompt {i}/5")
        
        # Send to client
        resources = {"system_prompt": PromptTemplate(template=prompt, engine="f-string")}
        await server.update_resources(resources)
        task_id = await server.queue_task(sample={"prompt": test_question}, mode="train")
        
        # Get result
        rollout = await server.poll_completed_rollout(task_id, timeout=20)
        score = rollout.final_reward if rollout else 0.0
        
        results.append((prompt, score))
        print(f"   Score: {score:.2f}")
    
    # Show results
    results.sort(key=lambda x: x[1], reverse=True)
    print(f"\n📊 RESULTS:")
    for i, (prompt, score) in enumerate(results, 1):
        preview = prompt[:50].replace('\n', ' ') + "..."
        print(f"   {i}. {score:.2f} - {preview}")
    
    best_prompt, best_score = results[0]
    worst_prompt, worst_score = results[-1]
    
    print(f"\n🏆 Best: {best_score:.2f}")
    print(f"📉 Worst: {worst_score:.2f}")
    
    # Evolution
    if best_score > worst_score + 0.1:  # Only evolve if clear difference
        print(f"\n🧬 EVOLUTION")
        new_prompts = await optimizer.evolve_prompts(best_prompt, worst_prompt, best_score, worst_score)
        
        if new_prompts:
            print(f"✅ Created {len(new_prompts)} evolved prompts")
            
            # Test evolved prompts
            print(f"\n🧪 Testing evolved prompts")
            best_evolved_score = 0.0
            
            for i, evolved_prompt in enumerate(new_prompts, 1):
                resources = {"system_prompt": PromptTemplate(template=evolved_prompt, engine="f-string")}
                await server.update_resources(resources)
                task_id = await server.queue_task(sample={"prompt": test_question}, mode="train")
                
                rollout = await server.poll_completed_rollout(task_id, timeout=20)
                evolved_score = rollout.final_reward if rollout else 0.0
                
                print(f"   Evolved {i}: {evolved_score:.2f}")
                best_evolved_score = max(best_evolved_score, evolved_score)
            
            # Show improvement
            improvement = best_evolved_score - best_score
            if improvement > 0:
                print(f"\n🎉 IMPROVEMENT: +{improvement:.2f} ({improvement/best_score*100:+.1f}%)")
            else:
                print(f"\n📊 No improvement this round")
        else:
            print("❌ Evolution failed")
    else:
        print(f"\n⏭️  Scores too similar, skipping evolution")
    
    # Cleanup
    await server.stop()
    print(f"\n✅ Complete")

if __name__ == "__main__":
    print("⚠️  Start 'python run_client.py' in another terminal first!")
    input("Press Enter when client is ready...")
    
    asyncio.run(run_evolution())