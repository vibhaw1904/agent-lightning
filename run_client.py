import dotenv
import os
import anthropic
from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer
from prompt_optimizer import calculate_reward

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
            
            # Calculate reward
            reward = calculate_reward(answer, task["prompt"])
            
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