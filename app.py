import os
# app.py  ──────────────────────────────────────────────────────────────
from flask import Flask, render_template, request, abort

app = Flask(__name__)

# 1️⃣  List each question sentence in order
# Your 17 questions
RAW_QUESTIONS = [
    "Do you have Two or more attacks at more than 24 hrs apart?",
    "Do you have Single attack only?",
    "Do you have Unconsciousness or drowsiness during episode?",
    "Do you have jerky movements of limbs & with tonic posturing or forced head turning?",
    "Do you have Jerky or tonic posturing on one side then involving the other side?",
    "Do you have Frothing or tongue bite or urine incontinence during the attack or attack during sleep",
    "Do you have confusion or fatigue after the attack?",
    "Do you have head injury or neurological problem?",
    "Do you have Flailing or side-to-side movements or rapid breathing during attack?",
    "Do you have attack with emotional stress or in public?",
    "Do you have depression or anxiety?",
    "Are you able to hear or see during the attack?",
    "Do you have loss of consciousness while standing or exerting?",
    "Do you have heart disease or heart rate or ECG irregularity?",
    "Is your EEG showing abnormal epileptic discharges (spikes and/Or sharp waves)?",
    "Is your MRI or CT Scan brain is abnormal?",
    "Do you have abnormal liver or kidney reports?"
]
QUESTIONS = [{"key": f"q{i}", "text": txt} for i, txt in enumerate(RAW_QUESTIONS, 1)]
KEYS      = [q["key"] for q in QUESTIONS]

def allowed_file(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ──────────────────────────────────────────────────────────────
# 3️⃣  Decision engine – write any logical expression you like
def diagnose(ans):
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17 = (
        ans[k] for k in KEYS
    )
    if not (q1 or q2 or q3):
        return "The EEG is normal!"
    else:
        if (q4 or q6 or q8 or q15 or q16):
            return "Strongly supportive of Generalised Epilepsy"
        elif q5:
            return "Strongly supportive of Focal Epilepsy"
        elif q7:
            return "Suggestive of Epilepsy" #use model
        elif (q9 or q12):
            return "Strongly suggestive of Psychogenic Non-Epileptic Attack"
        elif (q10 or q11):
            return "Supportive of Psychogenic Non-epileptic Attack" #use model
        elif q13:
            return "Supportive of Non-Epileptic Attack" #use model
        elif q14:
            return "Strongly supportive of Cardiogenic Non-Epileptic Attack"
        elif q17:
            return "Strongly supportive of Non-epileptic Attack - Likely Metabolic Encephalopathy"
        else:
            return "Supportive of Non-epileptic Attack" #use model

# ──────────────────────────────────────────────────────────────
# 4️⃣  Routes (unchanged UI except radio `name` = q1, q2, …)
@app.route("/", methods=["GET"])
def form():
    return render_template("index.html", questions=QUESTIONS)


@app.route("/diagnose", methods=["POST"])
def result():
    ans = {key: (request.form.get(key) == "yes") for key in KEYS}
    try:
        decision = diagnose(ans)
    except Exception as e:
        return render_template("index.html",
                               questions=QUESTIONS,
                               error=str(e)), getattr(e, "code", 500)

    answers_display = [(q["text"], "Yes" if ans[q["key"]] else "No") for q in QUESTIONS]
    return render_template("result.html",
                           decision=decision,
                           answers=answers_display)

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)