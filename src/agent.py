import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants - paths relative to project root
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(_project_root, "models", "model.txt")
TRAINING_DATA_PATH = os.path.join(_project_root, "data", "training_data.json")
OFFENSIVE_WORDS = ["hate", "kill", "die", "hurt", "violence"]

# Thread lock for safe file operations
file_lock = threading.Lock()

class TindAgent:
    """AI agent for generating conversation responses and handling user feedback."""
    
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        """Initialize the agent with a model."""
        self.model_path = Path(model_path)
        self.model_content = self._load_model()
        
    def _load_model(self) -> Optional[str]:
        """Load model from file with proper error handling."""
        try:
            if not self.model_path.exists():
                logger.warning(f"Model file not found at {self.model_path}")
                return None
                
            with open(self.model_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                logger.info(f"Model loaded successfully from {self.model_path}")
                return content
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None

    def generate_responses(self, context: str, num_responses: int = 5) -> List[str]:
        """Generate responses based on context with improved logic."""
        if not context or not context.strip():
            return ["I'd love to chat! What's on your mind?"]
            
        context_lower = context.lower().strip()
        
        # More sophisticated response generation based on context
        if any(word in context_lower for word in ["sad", "down", "upset", "depressed"]):
            responses = [
                "I'm sorry to hear that. Is there anything I can do to help?",
                "It's okay to feel sad sometimes. I'm here for you.",
                "Sending you a virtual hug. 🤗",
                "I'm here to listen if you want to talk about it.",
                "Remember that this feeling will pass. You're stronger than you know.",
            ]
        elif any(word in context_lower for word in ["hello", "hi", "hey", "oi"]):
            responses = [
                "Hi there! Great to meet you! How's your day going?",
                "Hey! You seem interesting - what brings you here today?",
                "Hello! I was just thinking this conversation needed someone like you.",
                "Hi! I have to say, you have great timing. What's up?",
                "Hey there! Ready for an amazing conversation?",
            ]
        elif any(word in context_lower for word in ["happy", "good", "great", "awesome"]):
            responses = [
                "That's wonderful to hear! Your positive energy is contagious.",
                "I love your enthusiasm! What's making you so happy?",
                "Your good mood just made my day better too!",
                "That's amazing! I'd love to hear more about what's going well.",
                "Your happiness is infectious - keep spreading those good vibes!",
            ]
        else:
            # Default conversation starters
            responses = [
                "That's interesting! Tell me more about that.",
                "I find that fascinating. What's your take on it?",
                "You have a unique perspective. I'd love to hear more.",
                "That caught my attention. What made you think of that?",
                "Interesting point! How did you come to that conclusion?",
            ]
        
        # Ensure we return the requested number of responses
        while len(responses) < num_responses:
            responses.extend(responses[:num_responses - len(responses)])
            
        return responses[:num_responses]

    def filter_responses(self, responses: List[str]) -> List[str]:
        """Filter out potentially offensive responses."""
        filtered_responses = []
        
        for response in responses:
            if any(word in response.lower() for word in OFFENSIVE_WORDS):
                filtered_responses.append("I'd prefer to keep our conversation positive and respectful.")
                logger.warning(f"Filtered offensive response: {response}")
            else:
                filtered_responses.append(response)
                
        return filtered_responses

    def save_conversation(self, context: str, responses: List[str], best_response: str) -> bool:
        """Save conversation data with thread safety and error handling."""
        if not context or not responses or not best_response:
            logger.error("Invalid conversation data provided")
            return False
            
        conversation_data = {
            "context": context.strip(),
            "responses": responses,
            "best_response": best_response.strip(),
            "timestamp": self._get_timestamp()
        }
        
        try:
            with file_lock:
                # Ensure data directory exists
                data_dir = Path(TRAINING_DATA_PATH).parent
                data_dir.mkdir(exist_ok=True)
                
                # Load existing data or create new list
                existing_data = self._load_training_data()
                existing_data.append(conversation_data)
                
                # Write back to file
                with open(TRAINING_DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                    
                logger.info("Conversation data saved successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return False

    def _load_training_data(self) -> List[Dict[str, Any]]:
        """Load existing training data or return empty list."""
        try:
            if Path(TRAINING_DATA_PATH).exists():
                with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            
        return []

    def _get_timestamp(self) -> str:
        """Get current timestamp for data tracking."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_user_feedback_cli(self, responses: List[str]) -> Optional[str]:
        """Get user feedback via command line interface."""
        print("\nPlease choose the best response:")
        for i, response in enumerate(responses, 1):
            print(f"{i}. {response}")
        print("0. None of the above")

        while True:
            try:
                choice = input("\nEnter your choice (0-{}): ".format(len(responses)))
                choice_num = int(choice)
                
                if choice_num == 0:
                    return None
                elif 1 <= choice_num <= len(responses):
                    return responses[choice_num - 1]
                else:
                    print(f"Please enter a number between 0 and {len(responses)}")
                    
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please enter a number.")
                continue

def main():
    """Main function for CLI usage."""
    agent = TindAgent()
    
    if not agent.model_content:
        print("Warning: No model loaded. Using default response generation.")
    
    print("Welcome to Tind AI! (Type 'quit' to exit)")
    
    while True:
        try:
            context = input("\nEnter conversation context: ").strip()
            
            if context.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not context:
                print("Please enter some context.")
                continue
                
            # Generate and filter responses
            responses = agent.generate_responses(context)
            filtered_responses = agent.filter_responses(responses)
            
            # Get user feedback
            best_response = agent.get_user_feedback_cli(filtered_responses)
            
            if best_response:
                success = agent.save_conversation(context, filtered_responses, best_response)
                if success:
                    print("✅ Feedback saved successfully!")
                else:
                    print("❌ Error saving feedback.")
            else:
                print("No response selected.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()
