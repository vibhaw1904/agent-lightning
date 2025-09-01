import asyncio

from agentlightning.server import AgentLightningServer
from agentlightning.types import NamedResources, PromptTemplate


async def example_apo():
    """
    An example of how a prompt optimization works.
    """
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    await server.start()

    # Different system prompt styles to test which works best
    prompt_candidates = [
        "You are a concise, analytical AI assistant. Provide clear, structured responses with key points organized in numbered lists. Focus on delivering factual information efficiently without unnecessary elaboration.",
        
        "You are an enthusiastic educator with deep expertise in technology and learning. Write in an engaging, accessible style that makes complex topics easy to understand. Use real-world examples and analogies to illustrate your points.",
        
        "You are a balanced, thoughtful AI that presents multiple perspectives on every topic. Always discuss both benefits and potential drawbacks. Structure your responses with clear pros and cons, and conclude with a nuanced summary.",
        
        "You are a creative storyteller who uses narrative techniques to explain concepts. Incorporate vivid examples, hypothetical scenarios, and engaging anecdotes to make your explanations memorable and compelling.",
        
        "You are a brief, direct AI assistant. Provide essential information only. Use bullet points and short paragraphs. Avoid redundancy and focus on actionable insights."
    ]

    prompt_and_rewards = []

    for i, prompt in enumerate(prompt_candidates, 1):
        # 1. The optimization algorithm updates the prompt template
        print(f"\n🔄 [Algo] Testing prompt {i}/{len(prompt_candidates)}")
        print(f"📝 [Algo] System prompt: '{prompt[:60]}...'")
        resources: NamedResources = {"system_prompt": PromptTemplate(template=prompt, engine="f-string")}
        await server.update_resources(resources)

        # 2. The algorithm queues up a task from a dataset
        print("📋 [Algo] Queuing evaluation task...")
        task_id = await server.queue_task(
            sample={"prompt": "Explain the impact of remote work on modern business culture, including productivity, collaboration, and work-life balance."}, 
            mode="train"
        )
        print(f"🆔 [Algo] Task '{task_id}' queued for processing")

        # 3. The algorithm waits for clients to process the task
        print("⏳ [Algo] Waiting for client response...")
        rollout = await server.poll_completed_rollout(task_id, timeout=30)
        assert rollout, "Expected a completed rollout from the client."
        
        reward = rollout.final_reward
        print(f"🎯 [Algo] Reward received: {reward:.3f}")
        prompt_and_rewards.append((prompt[:60] + "...", reward))

    print(f"\n🏆 [Algo] Final Results:")
    for i, (prompt, reward) in enumerate(prompt_and_rewards, 1):
        print(f"   {i}. '{prompt}' → Reward: {reward:.3f}")
    
    best_prompt = max(prompt_and_rewards, key=lambda x: x[1])
    print(f"\n🥇 [Algo] Best performing prompt:")
    print(f"   📝 Prompt: '{best_prompt[0]}'")
    print(f"   🎯 Reward: {best_prompt[1]:.3f}")

    await server.stop()


if __name__ == "__main__":
    print("🌟 Agent Lightning Prompt Optimization Demo")
    print("=" * 50)
    print("Testing different system prompt styles to find the best performer!")
    asyncio.run(example_apo())