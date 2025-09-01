import anthropic
from agentlightning.litagent import LitAgent
import random
import os

class SimpleAgent(LitAgent):
    def training_rollout(self, task, rollout_id, resources):
        """Execute a single training rollout."""
        print(f"\n🤖 [Client] Starting rollout {rollout_id}")
        print(f"📋 [Client] Task: {task}")
        
        try:
            # Extract the system prompt being tested
            system_prompt = resources["system_prompt"].template
            print(f"🎯 [Client] System prompt: '{system_prompt[:50]}...'")
            
            # Initialize Anthropic client
            print("🔑 [Client] Initializing Anthropic client...")
            client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            
            # Call Anthropic Claude with this prompt
            print("🚀 [Client] Calling Claude API...")
            result = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": task["prompt"]}
                ],
            )
            
            # Get response content
            response = result.content[0].text
            print(f"📝 [Client] Response received (length: {len(response)} chars)")
            print(f"💬 [Client] Response preview: '{response[:100]}...'")
            
            # Calculate a simple reward based on response length and quality
            # In practice, you'd implement more sophisticated evaluation
            reward = min(len(response) / 100, 1.0) + random.uniform(0, 0.1)
            print(f"🎯 [Client] Calculated reward: {reward:.3f}")
            
            result_data = {
                "reward": reward,
                "response": response,
                "task_id": task.get("id", rollout_id)
            }
            
            print(f"✅ [Client] Rollout {rollout_id} completed successfully!")
            return result_data
            
        except Exception as e:
            print(f"❌ [Client] Error in rollout {rollout_id}: {str(e)}")
            return {
                "reward": 0.0,
                "error": str(e),
                "task_id": task.get("id", rollout_id)
            }