import dotenv
import os
import random

from openai import OpenAI

from agentlightning import configure_logger
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer


class SimpleAgent(LitAgent):

    def training_rollout(self, task, rollout_id, resources):
        print(f"🤖 [Client] Starting rollout {rollout_id}")
        print(f"📋 [Client] Task: {task}")
        print(f"🎯 [Client] Resources: {resources}")

        try:
            # Use Anthropic instead of OpenAI
            import anthropic
            client = anthropic.Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY")
            )

            result = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system=resources["system_prompt"].template,
                messages=[
                    {"role": "user", "content": task["prompt"]}
                ],
            )
            
            response = result.content[0].text
            print(f"📝 [Client] Response: {response[:100]}...")

            # Calculate reward
            reward = min(len(response) / 100, 1.0) + random.uniform(0, 0.1)
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