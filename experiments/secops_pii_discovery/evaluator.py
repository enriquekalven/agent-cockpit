"""AlphaEvolve-compatible CLI evaluator for secops_pii_discovery."""
import argparse
import importlib.util
import json
import math
import os
import sys
import traceback
from typing import Any, Dict


def evaluate_program(program_code: str, timeout_seconds: int = 30) -> Dict[str, Any]:
    """Evaluates the evolved code snippet by dynamically exec'ing it and capturing output."""
    insights = []
    score = None
    
    # Setup standard output capturing
    from io import StringIO
    import contextlib
    
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            # 1. Parse and validate the code
            try:
                import ast
                ast.parse(program_code)
            except SyntaxError as e:
                insights.append({"label": "error", "text": f"Syntax Error: {e}"})
                insights.append({"label": "traceback", "text": traceback.format_exc()})
                return {"score": None, "insights": insights}
                
            # 2. Exec the program securely (isolation within a local dict namespace)
            namespace = {}
            exec(program_code, namespace)
            
            # 3. Invoke evaluate()
            if "evaluate" not in namespace:
                insights.append({"label": "error", "text": "Function 'evaluate(eval_inputs)' not found in program."})
                return {"score": None, "insights": insights}
                
            eval_fn = namespace["evaluate"]
            result = eval_fn({})
            
            if not isinstance(result, dict) or "f1_score" not in result:
                insights.append({"label": "error", "text": "evaluate() must return a dict containing 'f1_score'."})
                return {"score": None, "insights": insights}
                
            raw_score = result["f1_score"]
            
            if not isinstance(raw_score, (int, float)) or math.isnan(raw_score) or math.isinf(raw_score):
                 insights.append({"label": "error", "text": f"Non-finite or invalid score returned: {raw_score}"})
                 score = None
            else:
                 score = float(raw_score)

    except Exception as e:
        insights.append({"label": "error", "text": str(e)})
        insights.append({"label": "traceback", "text": traceback.format_exc()})
        score = None
        
    out_text = stdout_capture.getvalue()
    err_text = stderr_capture.getvalue()
    
    if out_text:
        insights.append({"label": "stdout", "text": out_text})
    if err_text:
        insights.append({"label": "stderr", "text": err_text})
        
    return {
        "score": score,
        "insights": insights
    }


def main():
    parser = argparse.ArgumentParser(description="AlphaEvolve Evaluator")
    parser.add_argument("--output-file", required=True, help="Path to write score JSON")
    parser.add_argument("--program-dir", required=True, help="Path containing initial_program.py")
    args = parser.parse_args()
    
    program_path = os.path.join(args.program_dir, "initial_program.py")
    if not os.path.exists(program_path):
        print(f"❌ Source file not found: {program_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(program_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    result = evaluate_program(code)
    
    out_dir = os.path.dirname(args.output_file)
    if out_dir:
         os.makedirs(out_dir, exist_ok=True)

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"✅ Evaluation complete. Score: {result['score']}")


if __name__ == "__main__":
    main()
