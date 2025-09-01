import anthropic
from agentlightning.litagent import LitAgent
from agentlightning.trainer import Trainer
import random
import os

class SimpleAgent(LitAgent):
    def training_rollout(self, task, rollout_id, resources):
        """Execute a single training rollout."""
        try:
            # Extract the system prompt being tested
            system_prompt = resources["system_prompt"].template
            
            # Initialize Anthropic client
            client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            
            # Call Anthropic Claude with this prompt
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
            
            # Calculate a simple reward based on response length and quality
            # In practice, you'd implement more sophisticated evaluation
            reward = min(len(response) / 100, 1.0) + random.uniform(0, 0.1)
            
            return {
                "reward": reward,
                "response": response,
                "task_id": task.get("id", rollout_id)
            }
            
        except Exception as e:
            return {
                "reward": 0.0,
                "error": str(e),
                "task_id": task.get("id", rollout_id)
            }

def main():
    # Create agent instance
    agent = SimpleAgent()
    
    # Set up trainer with distributed workers
    trainer = Trainer(n_workers=2)
    
    # Example tasks for training
    example_tasks = [
        {"prompt": "Explain the concept of machine learning in simple terms", "id": "task_1"},
        {"prompt": "What are the benefits of distributed computing?", "id": "task_2"},
        {"prompt": "How does reinforcement learning work?", "id": "task_3"}
    ]
    
    # Start training (you would typically run this with a server backend)
    print("Starting Agent Lightning training...")
    
    # For demonstration, run a single rollout
    sample_resources = {
        "system_prompt": type('obj', (object,), {"template": "You are a helpful AI assistant that provides clear and concise explanations."})()
    }
    
    result = agent.training_rollout(example_tasks[0], "demo_rollout", sample_resources)
    print(f"Training result: {result}")

if __name__ == "__main__":
    main()

