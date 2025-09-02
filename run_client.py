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
            # Use OpenAI client with Nugen API
            api_key = os.environ.get("NUGEN_API_KEY")
            model_name = "Llama-V3p1-8b-Instruct"
            base_url = os.environ.get("NUGEN_API_BASE")
            
            # Add the specific Nugen endpoint path
            if base_url and not base_url.endswith('/api/v3/inference/completions'):
                if base_url.endswith('/'):
                    base_url = base_url + 'api/v3/inference/completions'
                else:
                    base_url = base_url + '/api/v3/inference/completions'
            
            print(f"🤖 [Client] Using Nugen API with OpenAI client")
            print(f"🔗 [Client] Base URL: {base_url}")
            print(f"🤖 [Client] Model: {model_name}")
            
            # Initialize OpenAI client with custom base URL
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.dev-nugen.in/api/v3/inference/"
            )
            
            # Construct the messages
            system_prompt = resources["system_prompt"].template
            user_prompt = task["prompt"]
            
            print(f"🚀 [Client] Making OpenAI request...")
            response = client.completions.create(
                model=model_name,
                prompt=f"{system_prompt}\n{user_prompt}",
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response text from OpenAI response
            response_text = response.choices[0].text
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