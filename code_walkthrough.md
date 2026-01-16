# Code Walkthrough

A concise guide to understanding the text-to-SQL evaluation system codebase.

## Project Structure

```
.
├── main.py                 # Main orchestration script
├── src/
│   ├── sql_generator.py   # SQL generation using LLM
│   ├── sql_response.py    # SQL execution
│   ├── sql_evaluator.py   # Evaluation metrics
│   ├── prompts.py         # Prompt templates
│   ├── model_outputs.py   # Excel output generation
│   └── models.yaml        # Model configuration
├── utils.py               # Database utilities
├── evaluation_data.json   # Test cases with ground truth
├── generate_eval_data.py  # Script to generate evaluation data
└── src/
    └── custom_test_cases.py  # Custom test cases for evaluation
```

## Main Entry Point: `main.py`

Orchestrates the evaluation workflow:

1. Loads test cases and model configurations
2. For each model:
   - Generates SQL using all prompts for each test case
   - Executes and evaluates each SQL query
   - Aggregates results
3. Saves summary statistics to Excel

**Key Features:**
- Rate limiting (10s between models, 2s between API calls)
- Batch processing of all test cases
- Comprehensive logging

## Source Files

### `sql_generator.py` - SQL Generation

**Purpose**: Generates SQL queries from natural language using FireworksAI API.

**Key Functions:**
- `load_model_config()` - Loads model configuration from YAML
- `extract_sql(response_text)` - Cleans SQL from LLM responses (handles markdown, XML tags)
- `generate_sql(question, prompts, model_name)` - Core generation function
  - Loads schema once
  - Calls API for each prompt
  - Returns dictionary: `{prompt_name: sql_query}`

### `sql_response.py` - SQL Execution

**Purpose**: Executes SQL queries against the database.

**Function:**
- `get_answer(sql_query)` - Executes SQL, returns results or error string

### `sql_evaluator.py` - Evaluation Metrics

**Purpose**: Calculates accuracy metrics.

**Key Functions:**
- `normalize_sql(sql)` - Normalizes SQL for comparison
- `calculate_sql_match_percent()` - Token-based SQL similarity (0-100%)
- `calculate_answer_match_percent()` - Value-based result matching (0-100%)
- `evaluate_answer()` - Returns: `{syntax_ok, sql_match_percent, answer_match_percent}`

**Metrics:**
1. **Syntax Check**: Does SQL execute? (binary)
2. **SQL Match**: How similar is generated SQL to expected? (token-based)
3. **Answer Match**: Do results match? (most important - value-based)

### `prompts.py` - Prompt Strategies

**Purpose**: Defines three prompt types.

1. **`basic_prompt`** - Simple, direct prompt (baseline)
2. **`few_shot_prompt`** - Includes 3 examples with structured output
3. **`agentic_prompt`** - Step-by-step reasoning approach

All prompts follow: `(schema_text: str, question: str) -> str`

### `model_outputs.py` - Results Export

**Purpose**: Saves evaluation results to Excel.

**Function:**
- `save_results_to_excel(prompt_results, file_identifier)`
- Creates Excel with summary: Model Name, Prompt Type, Avg SQL Match, Avg Answer Match

### `models.yaml` - Configuration

Centralized model and parameter configuration:
- Model paths (e.g., `gpt-oss-120b`, `deepseek-v3p1-terminus`)
- Parameters (temperature, max_tokens, etc.)

## Utility Files

- **`utils.py`**: Database connection, schema extraction, query execution
- **`evaluation_data.json`**: Test cases with `question`, `sql`, `expected_result`
  - Includes 10 original test cases plus 5 custom test cases
- **`generate_eval_data.py`**: Script to validate SQL queries and generate evaluation dataset
- **`src/custom_test_cases.py`**: Custom test cases covering diverse SQL patterns:
  - HAVING clause queries (artists with more than 10 albums)
  - Multiple joins with aggregation (top customers by spending)
  - Date grouping and filtering (tracks sold per month)
  - String pattern matching (tracks containing specific words)
  - Aggregation with calculations (average track length conversions)

## Next Steps & Future Improvements
 Model Fine Tuning to create a custom model using Firework's API based on the available schema and model test cases and use it to generate SQL queries.

**Approach:**
1. **Data Preparation**: Expand to 100+ examples covering diverse query types
2. **Format**: Instruction-following dataset
   ```json
   {
     "instruction": "Convert question to SQL",
     "input": "Schema: {...}\nQuestion: ...",
     "output": "SELECT ..."
   }
   ```
3. **Model Selection**: Start with smaller models (Llama 3 8B, Mistral 7B)
4. **Evaluation**: Compare fine-tuned vs. base models on held-out set


## Running the Evaluation

```bash
# Activate virtual environment
source .venv/bin/activate

# Set API key
export FIREWORKS_API_KEY="your-api-key-here"
# Or add to .env file

# Run evaluation
python main.py
```

**Output**: `model_output/all_models_results.xlsx` with summary statistics.