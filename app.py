import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# 設定 Gemini API (從環境變數讀取)
# 如果沒有設定 API Key，AI 功能會顯示提示，但網頁仍可正常開啟
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    ai_response = ""
    # 處理使用者的輸入
    if request.method == 'POST':
        if api_key:
            try:
                user_input = request.form.get('fitness_data')
                # 這是給 AI 的指令 (Prompt)
                prompt = f"我是一位體育老師，請針對以下學生的體適能數據提供專業建議，請用條列式並給予鼓勵的語氣：{user_input}"
                response = model.generate_content(prompt)
                ai_response = response.text
            except Exception as e:
                ai_response = f"AI 連線發生錯誤：{str(e)}"
        else:
            ai_response = "請記得在 Cloud Run 設定 GEMINI_API_KEY 環境變數，AI 才能運作喔！"

    # 你的作品集展示資料
    projects = [
        {"title": "校園資源回收管理系統", "desc": "自動化追蹤回收量與獎勵機制，提升校園環保效率。"},
        {"title": "國英雙語互動測驗系統", "desc": "結合自動出題與解析，減輕教師負擔。"},
        {"title": "Project Phoenix", "desc": "老舊電腦系統優化工具，延長設備使用壽命。"}
    ]
    
    return render_template('index.html', projects=projects, ai_response=ai_response)

if __name__ == "__main__":
    # 設定 Port，符合 Cloud Run 要求
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))