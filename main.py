from flask import Flask, render_template, request
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import re

app = Flask(__name__)

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="blanchefort/rubert-base-cased-sentiment"
)

tokenizer = AutoTokenizer.from_pretrained(
    "sberbank-ai/rugpt3medium_based_on_gpt2"
)
model = AutoModelForCausalLM.from_pretrained(
    "sberbank-ai/rugpt3medium_based_on_gpt2"
)


def extract_film_title(text):
    if not text:
        return ""
    m = re.search(r'"([^"]{2,100})"', text)
    if m:
        return m.group(1)
    return text.strip().splitlines()[0][:80]


def generate_recommendation(mood):
    prompt = f"Посоветуй фильм для человека у которого {mood} настроение и кратко объясни почему"

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_length=80,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
        pad_token_id=tokenizer.eos_token_id
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text[len(prompt):].strip()


@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    user_text = ""

    if request.method == "POST":
        user_text = request.form.get("message", "")

        result = sentiment_analyzer(user_text)[0]
        label = result["label"]

        if label == "POSITIVE":
            mood = "хорошее"
        elif label == "NEGATIVE":
            mood = "плохое"
        else:
            mood = "нейтральное"

        rec = extract_film_title(generate_recommendation(mood))
        recommendation = f"Настроение: {mood}<br>Фильм: {rec}"

    return render_template(
        "index.html",
        recommendation=recommendation,
        user_text=user_text
    )


if __name__ == "__main__":
    app.run(debug=True)