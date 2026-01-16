import os
import yaml
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from utils import load_db, get_schema

load_dotenv()


def load_model_config():
    """Load model configuration from YAML file."""
    config_path = Path(__file__).parent / "models.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def extract_sql(response_text: str) -> str:
    """Extract SQL from API response, removing brackets and newlines at start/end."""
    sql = response_text.strip()
    
    # Extract from markdown code blocks
    sql_match = re.search(r'```(?:sql)?\s*(.*?)\s*```', sql, re.DOTALL)
    if sql_match:
        sql = sql_match.group(1).strip()
    
    # Extract from sql_query tags
    tag_match = re.search(r'<sql_query>\s*(.*?)\s*</sql_query>', sql, re.DOTALL | re.IGNORECASE)
    if tag_match:
        sql = tag_match.group(1).strip()
    
    # Remove any remaining angle bracket tags
    sql = re.sub(r'<[^>]*>', '', sql)
    
    # Remove brackets and newlines from beginning
    while sql and sql[0] in '<[{}\n':
        sql = sql[1:].strip()
    
    # Remove brackets and newlines from end
    while sql and sql[-1] in '>]}\n':
        sql = sql[:-1].strip()
    
    return sql


def generate_sql(question: str, prompts: list, model_name: str, db_path: str = "Chinook.db"):
    """
    Generate SQL from natural language question using all provided prompts.
    
    Args:
        question: Natural language question
        prompts: List of tuples (prompt_name, prompt_func)
        model_name: Name of the model to use
        db_path: Path to database
        
    Returns:
        Dictionary mapping prompt names to generated SQL queries
    """
    api_key = os.getenv("FIREWORKS_API_KEY")
    if not api_key:
        raise ValueError("FIREWORKS_API_KEY not set")
    
    # Load model config
    config = load_model_config()
    
    # Get model from config
    model = config["model"][model_name]
    
    # Get schema (only once)
    conn = load_db(db_path)
    schema = get_schema(conn)
    schema_text = "\n".join([f"{table}: {[c['name'] for c in cols]}" for table, cols in schema.items()])
    conn.close()
    
    # Initialize client
    client = OpenAI(api_key=api_key, base_url="https://api.fireworks.ai/inference/v1")
    
    # Store results for all prompts
    results = {}
    
    # Generate SQL for each prompt
    for prompt_name, prompt_func in prompts:
        # Create prompt using the provided function
        prompt = prompt_func(schema_text, question)
        
        # Call API
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            top_p=config.get("top_p", 1),
            presence_penalty=config.get("presence_penalty", 0),
            frequency_penalty=config.get("frequency_penalty", 0)
        )
        
        sql = extract_sql(response.choices[0].message.content)
        results[prompt_name] = sql
        
        # Delay to prevent rate limits
        time.sleep(5)
    
    return results

