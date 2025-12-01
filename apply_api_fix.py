import re

# Read the file
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find and replace
old_pattern = r'''    try:
        logger\.info\(f"Searching for: \{query\}"\)
        response = requests\.post\(LEAKOSINT_API_URL, json=data, timeout=30\)
        response\.raise_for_status\(\)
        json_response = response\.json\(\)
        
        logger\.info\(f"API Response: \{json_response\}"\)
        
        # Check for errors
        if "Error code" in json_response:
            logger\.error\(f"API Error: \{json_response\['Error code'\]\}"\)
            return None'''

new_code = '''    try:
        logger.info(f"Searching for: {query}")
        response = requests.post(LEAKOSINT_API_URL, json=data, timeout=30)
        
        try:
            json_response = response.json()
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON response")
            logger.error(f"Raw response: {response.text[:500]}")
            return None
        
        logger.info(f"API Response: {json_response}")
        
        # Check for API errors (including 502 backend errors)
        if "error" in json_response:
            error_code = json_response.get("error")
            logger.error(f"API Error: {error_code}")
            return None
        
        if "Error code" in json_response:
            logger.error(f"API Error Code: {json_response['Error code']}")
            return None'''

# Replace
content = re.sub(old_pattern, new_code, content, flags=re.MULTILINE)

# Write back
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ API fix applied successfully!")
print("The bot now matches the working test_api.py pattern.")
