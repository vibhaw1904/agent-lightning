import asyncio
import dotenv
from agentlightning.trainer import Trainer
from agentlightning.server import AgentLightningServer
from agentlightning.types import PromptTemplate
from agentlightning  import configure_logger
from client import SimpleAgent


# def main():
#     # Create agent instance
#     agent = SimpleAgent()
    
#     # Set up trainer with distributed workers
#     trainer = Trainer(n_workers=2)
    
#     trainer.fit(agent,backend="http://127.0.0.1:9997")
#     # Example tasks for training
#     prompt_candidates = [
#         {"prompt": "Explain the concept of machine learning in simple terms", "id": "task_1"},
#         {"prompt": "What are the benefits of distributed computing?", "id": "task_2"},
#         {"prompt": "How does reinforcement learning work?", "id": "task_3"}
#     ]

    
    # Start training (you would typically run this with a server backend)
    # print("Starting Agent Lightning training...")
    
    # # For demonstration, run a single rollout
    # sample_resources = {
    #     "system_prompt": type('obj', (object,), {"template": "You are a helpful AI assistant that provides clear and concise explanations."})()
    # }
    
    # result = agent.training_rollout(example_tasks[0], "demo_rollout", sample_resources)
    # print(f"Training result: {result}")

   


async def prompt_optimization():
    print("🚀 Starting prompt optimization process...")
    
    prompt_candidates = [
        {"prompt": "Explain the concept of machine learning in simple terms", "id": "task_1"},
        {"prompt": "What are the benefits of distributed computing?", "id": "task_2"},
        {"prompt": "How does reinforcement learning work?", "id": "task_3"}
    ]
    print(f"📝 Loaded {len(prompt_candidates)} prompt candidates")
    
    prompt_and_rewards = []
    print("🖥️ Initializing AgentLightning server on 127.0.0.1:9997...")
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    print("⏳ Starting server...")
    await server.start()
    print("✅ Server started successfully!")
    
    print(f"\n🔄 Processing {len(prompt_candidates)} prompts...")
    for i, prompt in enumerate(prompt_candidates, 1):
        print(f"\n--- Processing Prompt {i}/{len(prompt_candidates)} ---")
        print(f"📋 Current prompt: '{prompt['prompt']}'")
        
        # Send this prompt to all connected clients
        print("📤 Creating prompt template and updating resources...")
        resources = {
            "system_prompt": PromptTemplate(template=prompt["prompt"], engine="f-string")
        }
        await server.update_resources(resources)
        print("✅ Resources updated successfully")
        
        # Queue a task for clients to process
        print("📋 Queuing task for client processing...")
        task_id = await server.queue_task(
            sample={"prompt": "What is the capital of France?"}, 
            mode="train"
        )
        print(f"🆔 Task queued with ID: {task_id}")

        # Wait for a client to complete it (30 second timeout)
        print("⏳ Waiting for client to complete rollout (30s timeout)...")
        rollout = await server.poll_completed_rollout(task_id, timeout=30)

        # Check if rollout was completed successfully
        if rollout is None:
            print(f"❌ Rollout timed out or failed for prompt: {prompt['prompt']}")
            reward = 0.0
        else:
            print("✅ Rollout completed successfully!")
            # Extract and store the reward (this comes from the return value of the client side)
            reward = rollout.final_reward
            print(f"🎯 Reward received: {reward}")
        
        prompt_and_rewards.append((prompt["prompt"], reward))
        print(f"📊 Prompt processed. Current results: {len(prompt_and_rewards)}/{len(prompt_candidates)}")
    
    print("\n🎉 All prompts processed!")
    print(f"📈 Final Results - All prompts and their rewards:")
    for prompt, reward in prompt_and_rewards:
        print(f"   • '{prompt}' → Reward: {reward:.3f}")
    
    if prompt_and_rewards:
        best_prompt = max(prompt_and_rewards, key=lambda x: x[1])
        print(f"\n🏆 Best performing prompt:")
        print(f"   📝 Prompt: '{best_prompt[0]}'")
        print(f"   🎯 Reward: {best_prompt[1]:.3f}")
    else:
        print("⚠️ No successful rollouts completed")

    print("\n🛑 Stopping server...")
    await server.stop()
    print("✅ Server stopped successfully!")


def main():
    print("🔧 Configuring logger...")
    configure_logger()
    print("📄 Loading environment variables...")
    dotenv.load_dotenv()
    print("✅ Initial setup complete!")
    
    print("\n⚠️ NOTE: Make sure to run the trainer/client in a separate terminal:")
    print("   python -c \"from client import SimpleAgent; from agentlightning.trainer import Trainer; agent=SimpleAgent(); trainer=Trainer(n_workers=2); trainer.fit(agent, backend='http://127.0.0.1:9997')\"")
    
    # Run the prompt optimization server
    print("\n🎬 Starting main optimization process...")
    asyncio.run(prompt_optimization())

if __name__ == "__main__":
    print("🌟 Agent Lightning Prompt Optimization Demo")
    print("=" * 50)
    main()
    print("\n🎬 Demo completed!")
    print("=" * 50)

