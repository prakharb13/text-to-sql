import json
import time
from pathlib import Path
from src.sql_generator import generate_sql, load_model_config
from src.sql_response import get_answer
from src.sql_evaluator import evaluate_answer
from src.model_outputs import save_results_to_excel
from src.prompts import basic_prompt, few_shot_prompt, agentic_prompt
from src.custom_test_cases import CUSTOM_TEST_CASES

# Load original evaluation data
eval_data_path = Path("evaluation_data.json")
with open(eval_data_path, 'r') as f:
    original_eval_data = json.load(f)

# Use only first 2 original test cases
original_eval_data = original_eval_data[:2]

# Convert custom test cases to evaluation format (expected_result already included)
# Use only first 2 custom test cases
custom_eval_data = [
    {
        "question": case["question"],
        "sql": case["sql"],
        "expected_result": case["expected_result"]
    }
    for case in CUSTOM_TEST_CASES[:2]
]

# Load model config
config = load_model_config()

# Define prompts to test
prompts = [
    ("prompt_1", basic_prompt),
    ("prompt_2", few_shot_prompt),
    ("prompt_3_agentic", agentic_prompt)
]

# Get all models from config
models = config["model"]

print(f"Evaluating {len(original_eval_data)} original + {len(custom_eval_data)} custom test cases with {len(prompts)} prompts across {len(models)} models...\n")
print("=" * 80)

def evaluate_test_cases(eval_data, test_type):
    """Evaluate test cases and return results."""
    results = {}
    
    for idx, (model_key, model_path) in enumerate(models.items()):
        model_name = model_path.split("/")[-1]
        print(f"\n{'='*80}")
        print(f"MODEL: {model_key} ({model_name}) - {test_type.upper()} TEST CASES")
        print(f"{'='*80}\n")
        
        prompt_results = {prompt_name: [] for prompt_name, _ in prompts}
        
        for i, test_case in enumerate(eval_data, 1):
            question = test_case["question"]
            expected_sql = test_case["sql"]
            expected_result = test_case["expected_result"]
            
            print(f"\nTest Case {i}/{len(eval_data)}")
            print(f"Question: {question}")
            
            print("\n1. Generating SQL...")
            sql_results = generate_sql(question, prompts, model_key)
            print(f"SQL: {sql_results}")
            
            for prompt_name, sql in sql_results.items():
                print(f"\n2. Executing SQL from {prompt_name}...")
                answer = get_answer(sql)
                
                print(f"\n3. Evaluating {prompt_name}...")
                evaluation = evaluate_answer(
                    answer,
                    generated_sql=sql,
                    expected_sql=expected_sql,
                    expected_result=expected_result
                )
                print(f"Syntax OK: {evaluation['syntax_ok']}")
                print(f"SQL Match: {evaluation['sql_match_percent']:.1f}%")
                print(f"Answer Match: {evaluation['answer_match_percent']:.1f}%")
                
                prompt_results[prompt_name].append({
                    'sql_match': evaluation['sql_match_percent'],
                    'answer_match': evaluation['answer_match_percent']
                })
            
            print("=" * 80)
        
        results[model_key] = prompt_results
        
        if idx < len(models) - 1:
            print(f"\nWaiting 20 seconds before next model...")
            time.sleep(20)
    
    return results

# Evaluate original test cases
print("\n" + "="*80)
print("EVALUATING ORIGINAL TEST CASES")
print("="*80)
original_results = evaluate_test_cases(original_eval_data, "original")

# Evaluate custom test cases
print("\n" + "="*80)
print("EVALUATING CUSTOM TEST CASES")
print("="*80)
custom_results = evaluate_test_cases(custom_eval_data, "custom")

# Convert to prompt_results format
all_prompt_results = {}
original_prompt_results = {}
custom_prompt_results = {}

for model_key, prompt_results in original_results.items():
    for prompt_name, results in prompt_results.items():
        key = f"{model_key}__{prompt_name}"
        all_prompt_results[key] = results
        original_prompt_results[key] = results

for model_key, prompt_results in custom_results.items():
    for prompt_name, results in prompt_results.items():
        key = f"{model_key}__{prompt_name}"
        all_prompt_results[key] = all_prompt_results.get(key, []) + results
        custom_prompt_results[key] = results

save_results_to_excel(all_prompt_results, "all_models", original_prompt_results, custom_prompt_results)
