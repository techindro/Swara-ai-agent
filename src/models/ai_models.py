"""AI model wrapper for content generation."""
import openai
from loguru import logger
from src.config import config

class AIModel:
    """Handles interaction with various AI providers (OpenAI, Gemini, etc.)."""
    
    def __init__(self):
        self.provider = "openai"
        if config.ai.openai_api_key:
            openai.api_key = config.ai.openai_api_key
        else:
            logger.warning("OPENAI_API_KEY not found in config.")

    async def generate(self, prompt: str, max_tokens: int = 280) -> str:
        """Generate content based on the prompt."""
        if not config.ai.openai_api_key:
            return f"[LOCAL PREVIEW] Content for: {prompt[:50]}..."
            
        try:
            response = openai.chat.completions.create(
                model=config.ai.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or config.ai.max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return f"Error: Could not generate content. {str(e)}"
