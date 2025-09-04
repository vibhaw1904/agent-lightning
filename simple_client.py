import dotenv
import os
import anthropic
from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer
from simple_optimizer import calculate_simple_reward

class SimpleAgent(LitAgent):
    
    def training_rollout(self, task, rollout_id, resources):
        print(f"\n🤖 [Client] Starting rollout {rollout_id}")
        print(f"   📋 Question: '{task['prompt']}'")
        print(f"   🎯 System prompt: '{resources['system_prompt'].template}'")
        
        try:
            # Use Anthropic Claude
            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            
            print(f"   🚀 Asking Claude...")
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                system=resources["system_prompt"].template,
                messages=[{"role": "user", "content": task["prompt"]}]
            )
            
            answer = response.content[0].text
            print(f"   💬 Claude answered: '{answer[:50]}...'")
            
            # Calculate reward using our simple system
            reward = calculate_simple_reward(answer, task["prompt"])
            print(f"   🎯 Final reward: {reward:.2f}")
            
            return reward
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return 0.0

if __name__ == "__main__":
    print("🤖 Simple Client Starting...")
    configure_logger()
    dotenv.load_dotenv()
    
    agent = SimpleAgent()
    trainer = Trainer(n_workers=1)  # Just 1 worker to keep it simple
    
    print("🔗 Connecting to server...")
    trainer.fit(agent, backend="http://127.0.0.1:9997")