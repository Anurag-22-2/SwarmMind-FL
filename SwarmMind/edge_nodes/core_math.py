import sys
import json

try:
    
    raw_arg = sys.argv[1]
    try:
        user_prompt = json.loads(raw_arg)
    except:
        user_prompt = raw_arg
        
    print(f"AI response for: {user_prompt}")
    sys.stdout.flush()
except Exception as e:
    sys.stderr.write(f"CRITICAL ERROR: {str(e)}\n")
    sys.exit(1)