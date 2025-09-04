import asyncio
from agentlightning.server import AgentLightningServer
from agentlightning.types import NamedResources, PromptTemplate
from prompt_optimizer import PromptOptimizer


async def evolutionary_prompt_optimization():
    """
    Advanced prompt optimization with evolutionary algorithm
    """
    print("🌟 Agent Lightning - Evolutionary Prompt Optimization")
    print("=" * 60)
    
    # Initialize components
    print("🔧 [Main] Initializing system components...")
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    optimizer = PromptOptimizer()
    
    print("🚀 [Main] Starting server...")
    await server.start()
    print("✅ [Main] Server started successfully!")
    
    # Initial prompt population (Generation 0)
    current_prompts = [
        "You are a concise, analytical AI assistant. Provide clear, structured responses with key points organized in numbered lists. Focus on delivering factual information efficiently without unnecessary elaboration.",
        
        "You are an enthusiastic educator with deep expertise in technology and learning. Write in an engaging, accessible style that makes complex topics easy to understand. Use real-world examples and analogies to illustrate your points.",
        
        "You are a balanced, thoughtful AI that presents multiple perspectives on every topic. Always discuss both benefits and potential drawbacks. Structure your responses with clear pros and cons, and conclude with a nuanced summary.",
        
        "You are a creative storyteller who uses narrative techniques to explain concepts. Incorporate vivid examples, hypothetical scenarios, and engaging anecdotes to make your explanations memorable and compelling.",
        
        "You are a brief, direct AI assistant. Provide essential information only. Use bullet points and short paragraphs. Avoid redundancy and focus on actionable insights."
    ]
    
    print(f"🧬 [Main] Starting with {len(current_prompts)} initial prompts")
    
    # Evolution parameters
    num_generations = 4
    evaluation_query = "Explain the impact of remote work on modern business culture, including productivity, collaboration, and work-life balance."
    
    print(f"🎯 [Main] Evaluation query: \"{evaluation_query[:50]}...\"")
    print(f"⏳ [Main] Planning {num_generations} generations of evolution")
    
    best_overall_score = 0.0
    best_overall_prompt = ""
    evolution_log = []
    
    # Evolutionary loop
    for generation in range(num_generations):
        print(f"\n{'='*60}")
        print(f"🧬 GENERATION {generation + 1}/{num_generations}")
        print(f"{'='*60}")
        
        print(f"📝 [Gen{generation+1}] Testing {len(current_prompts)} prompts...")
        
        # Test all prompts in current generation
        generation_results = []
        
        for i, prompt in enumerate(current_prompts):
            print(f"\n🔬 [Gen{generation+1}] Testing Prompt {i+1}/{len(current_prompts)}")
            print(f"💭 [Gen{generation+1}] Prompt preview: \"{prompt[:60]}...\"")
            
            # Update resources with current prompt
            resources: NamedResources = {
                "system_prompt": PromptTemplate(template=prompt, engine="f-string")
            }
            await server.update_resources(resources)
            
            # Queue task for evaluation
            print(f"📤 [Gen{generation+1}] Queuing evaluation task...")
            task_id = await server.queue_task(
                sample={"prompt": evaluation_query}, 
                mode="train"
            )
            
            # Wait for completion
            print(f"⏳ [Gen{generation+1}] Waiting for client response (30s timeout)...")
            rollout = await server.poll_completed_rollout(task_id, timeout=30)
            
            if rollout is None:
                print(f"❌ [Gen{generation+1}] Rollout timed out - assigning zero reward")
                reward = 0.0
            else:
                reward = rollout.final_reward
                print(f"✅ [Gen{generation+1}] Rollout completed successfully!")
            
            print(f"🏆 [Gen{generation+1}] Prompt {i+1} scored: {reward:.3f}")
            generation_results.append((prompt, reward))
            
            # Track best overall
            if reward > best_overall_score:
                best_overall_score = reward
                best_overall_prompt = prompt
                print(f"🎉 [Gen{generation+1}] NEW BEST SCORE! {reward:.3f}")
        
        # Sort results by performance
        generation_results.sort(key=lambda x: x[1], reverse=True)
        
        # Display generation summary
        print(f"\n📊 [Gen{generation+1}] GENERATION SUMMARY:")
        print(f"  🥇 Best: {generation_results[0][1]:.3f}")
        print(f"  📈 Average: {sum(r[1] for r in generation_results) / len(generation_results):.3f}")
        print(f"  📉 Worst: {generation_results[-1][1]:.3f}")
        
        # Show top 3 performers
        print(f"\n🏆 [Gen{generation+1}] TOP PERFORMERS:")
        for i, (prompt, score) in enumerate(generation_results[:3]):
            print(f"  {i+1}. Score {score:.3f}: \"{prompt[:50]}...\"")
        
        # Store evolution data
        evolution_log.append({
            'generation': generation + 1,
            'results': generation_results,
            'best_score': generation_results[0][1],
            'average_score': sum(r[1] for r in generation_results) / len(generation_results)
        })
        
        # Evolve new prompts for next generation (except for last generation)
        if generation < num_generations - 1:
            print(f"\n🧬 [Gen{generation+1}] EVOLVING NEXT GENERATION...")
            
            try:
                new_prompts = await optimizer.evolve_prompts(generation_results)
                
                if new_prompts:
                    current_prompts = new_prompts
                    print(f"✨ [Gen{generation+1}] Successfully evolved {len(new_prompts)} new prompts!")
                    
                    # Preview evolved prompts
                    print(f"\n🔮 [Gen{generation+1}] EVOLVED PROMPTS PREVIEW:")
                    for i, prompt in enumerate(new_prompts[:3]):
                        print(f"  {i+1}. \"{prompt[:60]}...\"")
                else:
                    print(f"⚠️ [Gen{generation+1}] Evolution failed, keeping current prompts")
                    
            except Exception as e:
                print(f"❌ [Gen{generation+1}] Evolution error: {e}")
                print(f"🔄 [Gen{generation+1}] Continuing with current prompts")
    
    # Final results
    print(f"\n{'='*60}")
    print("🎊 EVOLUTIONARY OPTIMIZATION COMPLETE!")
    print(f"{'='*60}")
    
    print(f"\n📈 EVOLUTION PROGRESS:")
    for log_entry in evolution_log:
        print(f"  Gen {log_entry['generation']}: Best={log_entry['best_score']:.3f}, Avg={log_entry['average_score']:.3f}")
    
    # Calculate improvement
    if len(evolution_log) >= 2:
        initial_avg = evolution_log[0]['average_score']
        final_avg = evolution_log[-1]['average_score']
        improvement = ((final_avg - initial_avg) / initial_avg * 100) if initial_avg > 0 else 0
        print(f"\n📊 OVERALL IMPROVEMENT: {improvement:+.1f}%")
    
    print(f"\n🏆 BEST OVERALL RESULT:")
    print(f"  🎯 Score: {best_overall_score:.3f}")
    print(f"  📝 Prompt: \"{best_overall_prompt[:100]}...\"")
    
    # Get evolution summary
    summary = optimizer.get_evolution_summary()
    if summary:
        print(f"\n🧬 EVOLUTION STATISTICS:")
        print(f"  📊 Total Generations: {summary['total_generations']}")
        print(f"  🎯 Best Score Achieved: {summary['best_overall_score']:.3f}")
        print(f"  📈 Improvement Trend: {len(summary['improvement_trend'])} data points")
    
    print(f"\n🛑 Stopping server...")
    await server.stop()
    print("✅ Server stopped successfully!")
    
    return {
        'best_prompt': best_overall_prompt,
        'best_score': best_overall_score,
        'evolution_log': evolution_log,
        'summary': summary
    }


if __name__ == "__main__":
    print("🌟 Agent Lightning - Evolutionary Prompt Optimization Demo")
    print("🧬 Automatically improving prompts through evolutionary algorithms")
    print("\n⚠️ IMPORTANT: Make sure to run 'python run_client.py' in another terminal!")
    
    input("\n🔄 Press Enter once you've started the client...")
    
    # Run the evolutionary optimization
    results = asyncio.run(evolutionary_prompt_optimization())
    
    print(f"\n🎬 Demo completed! Best evolved prompt achieved {results['best_score']:.3f} score")
    print("=" * 60)