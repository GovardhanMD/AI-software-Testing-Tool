import re
import json

def analyze_code(code_content):
    """Simple NLP-based code analysis"""
    functions = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', code_content)
    classes = re.findall(r'class\s+(\w+)', code_content)
    return {'functions': functions, 'classes': classes}

def generate_test_cases_simple(code_content, filename):
    """Generate test cases using simple pattern matching"""
    analysis = analyze_code(code_content)
    test_cases = []
    
    for func_name, params in analysis['functions']:
        test_cases.append({
            'name': f'test_{func_name}_valid_input',
            'type': 'functional',
            'description': f'Test {func_name} with valid input',
            'function': func_name,
            'expected': 'success'
        })
        test_cases.append({
            'name': f'test_{func_name}_invalid_input',
            'type': 'functional',
            'description': f'Test {func_name} with invalid input',
            'function': func_name,
            'expected': 'error_handling'
        })
    
    for class_name in analysis['classes']:
        test_cases.append({
            'name': f'test_{class_name}_initialization',
            'type': 'functional',
            'description': f'Test {class_name} object creation',
            'class': class_name,
            'expected': 'success'
        })
    
    if not test_cases:
        test_cases.append({
            'name': 'test_code_syntax',
            'type': 'non-functional',
            'description': 'Verify code has no syntax errors',
            'expected': 'success'
        })
    
    return test_cases

def generate_test_cases_ai(code_content, filename, api_key=None):
    """Generate test cases using AI (OpenAI API)"""
    if not api_key:
        return generate_test_cases_simple(code_content, filename)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Analyze this code and generate test cases in JSON format:

{code_content[:1000]}

Return ONLY a JSON array of test cases with this structure:
[{{"name": "test_name", "type": "functional/non-functional", "description": "test description", "expected": "expected result"}}]"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content.strip()
        result = re.sub(r'^```json\s*', '', result)
        result = re.sub(r'\s*```$', '', result)
        test_cases = json.loads(result)
        return test_cases
    except Exception as e:
        print(f"AI generation failed: {e}, falling back to simple generation")
        return generate_test_cases_simple(code_content, filename)

def generate_api_test_cases(api_spec):
    """Generate test cases for API specifications"""
    test_cases = []
    try:
        spec = json.loads(api_spec)
        endpoints = spec.get('endpoints', [])
        
        for endpoint in endpoints:
            method = endpoint.get('method', 'GET')
            path = endpoint.get('path', '/')
            
            test_cases.append({
                'name': f'test_{method.lower()}_{path.replace("/", "_")}',
                'type': 'functional',
                'description': f'Test {method} {path} with valid data',
                'endpoint': path,
                'method': method,
                'expected': '200'
            })
            test_cases.append({
                'name': f'test_{method.lower()}_{path.replace("/", "_")}_invalid',
                'type': 'functional',
                'description': f'Test {method} {path} with invalid data',
                'endpoint': path,
                'method': method,
                'expected': '400'
            })
    except:
        test_cases.append({
            'name': 'test_api_availability',
            'type': 'non-functional',
            'description': 'Test API is accessible',
            'expected': 'success'
        })
    
    return test_cases
