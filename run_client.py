import dotenv
import os
import anthropic
import asyncio
from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer
from advanced_prompt_optimizer import calculate_advanced_reward, simple_llm_judge_reward

class Agent(LitAgent):
    
    def training_rollout(self, task, rollout_id, resources):
        try:
            # Get Claude response
            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                system=resources["system_prompt"].template,
                messages=[{"role": "user", "content": task["prompt"]}]
            )
            
            answer = response.content[0].text
            print(f"📝 Response: {answer[:100]}...")
            
            # Choose evaluation method:
            # Option 1: Advanced detailed evaluation (slower but more comprehensive)
            reward = asyncio.run(calculate_advanced_reward(answer, task["prompt"], resources["system_prompt"].template))
            
            # Option 2: Simple LLM judge (faster, still sophisticated)
            # reward = asyncio.run(simple_llm_judge_reward(answer, task["prompt"]))
            
            print(f"🎯 LLM Judge Score: {reward:.2f}")
            return reward
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return 0.0

if __name__ == "__main__":
    print("🤖 Client starting...")
    configure_logger()
    dotenv.load_dotenv()
    
    agent = Agent()
    trainer = Trainer(n_workers=1)
    trainer.fit(agent, backend="http://127.0.0.1:9997")