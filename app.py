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
    "Do you have bilateral jerky movements of limbs & with tonic posturing or forced head turning?",
    "Do you have jerky or tonic posturing on one side then involving the other side?",
    "Do you have frothing or tongue bite or urine incontinence during the attack or attack during sleep",
    "Do you have confusion or fatigue after the attack?",
    "Do you have flailing or side-to-side movements or rapid breathing during attack?",
    "Do you have attack with emotional stress or in public?",
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
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15 = (
        ans[k] for k in KEYS
    )
    if not (q1 or q2 or q3 or q4 or q5 or q6 or q7 or q8 or q9 or q10 or q11 or q12 or q13 or q14 or q15):
        return "Multimodal AI model based EEG report is Normal!"
    else:
        if q13:
            return "Multimodal AI model based EEG report is strongly supportive of Epilepsy"
        else:
            if (q1 or q2 or q3) and (q4 or q5 or q6 or q7):
                return "Multimodal AI model based EEG report is strongly supportive of Epilepsy"
            elif q14 and (q1 or q2 or q3 or q4 or q5 or q6 or q7):
                return "Multimodal AI model based EEG report is strongly supportive of Epilepsy"
            elif (q1 and q4) or (q1 and q5) or (q1 and q6) or (q1 and q7):
                return "Multimodal AI model based EEG report is strongly supportive of Epilepsy"
            elif (q4 or q5 or q6 or q7):
                return "Multimodal AI model based EEG report is supportive of Epilepsy"
            elif not (q1 or q2 or q3) and (q8 or q9 or q10 or q11 or q12 or q15):
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack"
            elif (q1 or q2 or q3) and (q11 and q12) or (q11 and q15) or (q12 and q15) and ((q8 or q9 or q10) and q11) and ((q8 or q9 or q10) and q12) and ((q8 or q9 or q10) and q15):
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack"
            elif (q1 or q2 or q3) and (q8 or q9 or q10):
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack - Probable Psychogenic [Correlate clinically and get EEG with induction or Video EEG]"
            elif (q1 or q2 or q3) and q11:
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack - Probable Neurocardiogenic Syncope [Correlate with Echo/Holter/Autonomic Function Tests]"
            elif (q1 or q2 or q3) and q12:
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack - Probable Cardiogenic Syncope [Correlate with Echo/Holter]"
            elif (q1 or q2 or q3) and q15:
                return "Multimodal AI model based EEG report is strongly suggestive of Non-Epileptic Attack - Probable Metabolic Encephalopathy [Correlate with metabolic screening-LFT/KFT/Ammonia] "
            elif (q1 or q2 or q3):
                return "Use Model"  # use model
            elif q14:
                return "Use Model"  # use model

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
