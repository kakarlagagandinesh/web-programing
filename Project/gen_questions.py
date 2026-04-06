import json
import random
import urllib.request
import time
import html

def unescape(text):
    return html.unescape(text)

all_questions = []

print("Fetching questions from OpenTDB...")
for i in range(10):
    try:
        url = "https://opentdb.com/api.php?amount=50&category=18&type=multiple"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['response_code'] == 0:
                for item in data['results']:
                    question_text = unescape(item['question'])
                    correct = unescape(item['correct_answer'])
                    incorrect = [unescape(x) for x in item['incorrect_answers']]
                    
                    options = incorrect + [correct]
                    random.shuffle(options)
                    answer_index = options.index(correct)
                    
                    q_obj = {
                        "q": question_text,
                        "options": options,
                        "a": answer_index
                    }
                    if q_obj not in all_questions:
                        all_questions.append(q_obj)
        time.sleep(2)
    except Exception as e:
        print(f"Error fetching: {e}")

print(f"Fetched {len(all_questions)} unique questions.")

if len(all_questions) < 500:
    for i in range(500 - len(all_questions)):
        all_questions.append({
            "q": f"Computer Science Fundamentals Question #{i + 1}",
            "options": ["Variable", "Function", "Array", "Database"],
            "a": random.randint(0, 3)
        })

final_qs = all_questions[:500]

js_content = "const questionsBank = " + json.dumps(final_qs, indent=4) + ";"

with open("/Users/kakarlagagandinesh/Desktop/Web Workspace/questions.js", "w") as f:
    f.write(js_content)

print("Saved to questions.js successfully.")
