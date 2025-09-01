import asyncio

from agentlightning.server import AgentLightningServer
from agentlightning.types import NamedResources, PromptTemplate


async def example_apo():
    """
    An example of how a prompt optimization works.
    """
    server = AgentLightningServer(host="127.0.0.1", port=9997)
    await server.start()

    prompt_candidates = [
        "Write about technology. Explain how it works in life and everything around it. Talk about old and new things and maybe some future stuff too. You can also write about AI and internet because that is also technology. Just make sure to explain how people are using technology every day and what is good and bad about it. Add some examples like phone, computer, car, etc. The writing should be long enough to look detailed. Don’t forget to mention some advantages and disadvantages. Make it like an essay that anyone can understand but also with good words. Try to explain things but not too much in detail because it will be boring. Also, maybe say something about how technology helps students and workers, but you can also mention negative points like addiction or something. Overall just explain everything about technology in one go.",
        "Imagine you are a futurist education consultant in the year 2040. A global summit has invited you to deliver a short, inspiring essay (200 words) on the role of AI mentors in shaping the future of learning. In your essay, paint a vivid picture of how classrooms, online platforms, and personal study spaces have transformed because of AI. Describe how students in rural villages now access the same quality of education as elite urban schools, thanks to immersive AI-driven holographic tutors. Highlight a story of one fictional student—perhaps a 12-year-old in a remote area—whose life trajectory changes dramatically due to AI mentorship. Balance optimism with caution by acknowledging potential risks like dependency, bias in algorithms, or the fading role of human teachers. End with a powerful vision statement: a world where AI is not a replacement, but a bridge to unlock every child’s potential.",
        "You are a friendly chatbot.",
    ]

    prompt_and_rewards = []

    for prompt in prompt_candidates:
        # 1. The optimization algorithm updates the prompt template
        print(f"\n[Algo] Updating prompt template to: '{prompt}'")
        resources: NamedResources = {"system_prompt": PromptTemplate(template=prompt, engine="f-string")}
        # How the resource is used fully depends on the client implementation.
        await server.update_resources(resources)

        # 2. The algorithm queues up a task from a dataset
        print("[Algo] Queuing task for clients...")
        task_id = await server.queue_task(sample={"prompt": "How is artificial intelligence changing education in terms of accessibility, personalization, and challenges?"}, mode="train")
        print(f"[Algo] Task '{task_id}' is now available for clients.")

        # 3. The algorithm waits for clients to process the task
        rollout = await server.poll_completed_rollout(task_id, timeout=30)
        assert rollout, "Expected a completed rollout from the client."
        print(f"[Algo] Received Result: {rollout}")
        reward = rollout.final_reward
        prompt_and_rewards.append((prompt, reward))

    print(f"\n[Algo] All prompts and their rewards: {prompt_and_rewards}")
    best_prompt = max(prompt_and_rewards, key=lambda x: x[1])
    print(f"[Algo] Best prompt found: '{best_prompt[0]}' with reward {best_prompt[1]}")

    await server.stop()


if __name__ == "__main__":
    asyncio.run(example_apo())