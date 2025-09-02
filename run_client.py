import dotenv
import os
import random
import anthropic
from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer


class SimpleAgent(LitAgent):

    def training_rollout(self, task, rollout_id, resources):
        print(f"🤖 [Client] Starting rollout {rollout_id}")
        print(f"📋 [Client] Task: {task}")
        print(f"🎯 [Client] Resources: {resources}")

        try:
            # Use Anthropic Claude API
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            model_name = "claude-3-haiku-20240307"
            
            print(f"🤖 [Client] Using Anthropic Claude")
            print(f"🤖 [Client] Model: {model_name}")
            
            # Initialize Anthropic client
            client = anthropic.Anthropic(api_key=api_key)
            
            # Construct the messages
            system_prompt = resources["system_prompt"].template
            user_prompt = task["prompt"]
            
            print(f"🚀 [Client] Making Anthropic request...")
            response = client.messages.create(
                model=model_name,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            # Extract response text from Anthropic response
            response_text = response.content[0].text
            print(f"📝 [Client] Response: {response_text[:100]}...")

            # Calculate reward
            # we are calculating the reward based on response length it could be anything to calcualte reward
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