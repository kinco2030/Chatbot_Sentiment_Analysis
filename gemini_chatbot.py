import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API")
#print(GEMINI_API_KEY)

import google.generativeai as genai
from google.generativeai import types

import pandas as pd
import time
import json

def ask_gemini(prompt):
    start = time.time()
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        response = model.generate_content(
            generation_config=types.GenerationConfig(temperature=0.7),
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        end = time.time()
        content = response.candidates[0].content.parts[0].text

        prompt_tokens_response = model.count_tokens(
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        prompt_tokens = prompt_tokens_response.total_tokens

        completion_tokens_response = model.count_tokens(
            contents=[{"role": "model", "parts": [{"text": content}]}]
        )
        completion_tokens = completion_tokens_response.total_tokens
        
        total_tokens = prompt_tokens + completion_tokens

        return content, prompt_tokens, completion_tokens, total_tokens, end - start
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None, 0, 0, 0, 0
    
def main():
    genai.configure(api_key=GEMINI_API_KEY)

    # 착한 프롬프트
    # with open("data/kind_prompt.json", "r", encoding="utf-8") as f:
    #     prompts = json.load(f)

    # 나쁜 프롬프트
    with open("data/bad_prompt.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)

    results = []

    for prompt in prompts:
        print(f"실행 중: {prompt['type']} - {prompt['text']}")
        answer, prompt_tokens, completion_tokens, total_tokens, duration = ask_gemini(prompt["text"])
        results.append({
            "type": prompt["type"],
            "text": prompt["text"],
            "answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "duration": duration
        })
    
    df = pd.DataFrame(results)
    # df.to_excel("result/gemini_chatbot_results.xlsx", index=False, engine='openpyxl')
    df.to_excel("result/gemini_chatbot_bad_results.xlsx", index=False, engine='openpyxl')

if __name__ == "__main__":
    main()