import dotenv
import os
import random
import ollama
from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer


class SimpleAgent(LitAgent):

    def training_rollout(self, task, rollout_id, resources):
        print(f"🤖 [Client] Starting rollout {rollout_id}")
        print(f"📋 [Client] Task: {task}")
        print(f"🎯 [Client] Resources: {resources}")

        try:
            # Use Ollama with Llama 3.1 405B model
            model_name = "llama3.1:405b"
            
            print(f"🦙 [Client] Using Ollama with model: {model_name}")
            
            # Construct the full prompt with system and user messages
            system_prompt = resources["system_prompt"].template
            user_prompt = task["prompt"]
            
            print(f"🚀 [Client] Making Ollama request...")
            response = ollama.chat(
                model=model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt,
                    },
                    {
                        'role': 'user', 
                        'content': user_prompt,
                    }
                ],
                options={
                    'temperature': 0.7,
                    'num_predict': 1000,
                }
            )
            
            # Extract response text from Ollama response
            response_text = response['message']['content']
            print(f"📝 [Client] Response: {response_text[:100]}...")

            # Calculate reward
            reward = min(len(response_text) / 100, 1.0) + random.uniform(0, 0.1)
            print(f"🎯 [Client] Calculated reward: {reward}")

            # Return the reward directly (Agent Lightning handles the rollout completion)
            return reward

        except Exception as e:
            print(f"❌ [Client] Error: {e}")
            return 0.0


if __name__ == "__main__":
    configure_logger()
    dotenv.load_dotenv()
    agent = SimpleAgent()
    trainer = Trainer(n_workers=2)
    trainer.fit(agent, backend="http://127.0.0.1:9997")