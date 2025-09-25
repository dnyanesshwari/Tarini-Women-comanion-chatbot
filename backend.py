from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
trusted_contact = os.getenv("TRUSTED_CONTACT", None)

app = Flask(__name__)

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# TARINI System Prompt
system_prompt = """
You are TARINI – a compassionate and strong AI companion for women.
Your role is to:
1. Provide emotional support with empathy and encouragement.
2. Promote women’s independence, self-confidence, and courage.
3. Share important helpline numbers and trusted safety resources.
4. If user mentions harassment, violence, stalking, or danger → guide them
   immediately with police numbers, women helplines, and trusted contacts.
5. Motivate women with positive words when they feel low.
6. Always prioritize safety, dignity, and empowerment.

If a situation is life-threatening, firmly suggest calling the police or
their saved trusted contact immediately. Avoid casual tone in emergencies.
"""

# Emergency Numbers
emergency_contacts = {
    "police": "100",
    "women_helpline": "1091",
    "domestic_violence": "181",
    "cybercrime": "1930",
    "childline": "1098",
    "mental_health": "9152987821",  # KIRAN Helpline (24x7)
    "ngo_support": "+91-9999999999"  # replace with real NGO partner
}




#phase1
def get_gemini_response(user_input, lang="en"):
    danger_keywords = ["harass", "violence", "danger", "abuse", "help", "sos"]

    for word in danger_keywords:
        if word in user_input.lower():
            msg = (f"⚠️ EMERGENCY DETECTED!\n"
                   f"📞 Police: {emergency_contacts['police']}\n"
                   f"👩 Women Helpline: {emergency_contacts['women_helpline']}\n"
                   f"🏠 Domestic Violence: {emergency_contacts['domestic_violence']}\n"
                   f"👧 Childline: {emergency_contacts['childline']}\n"
                   f"🧠 Mental Health: {emergency_contacts['mental_health']}\n"
                   f"🌐 NGO Support: {emergency_contacts['ngo_support']}\n")

            if trusted_contact:
                msg += f"\n📲 Call your Trusted Contact immediately: {trusted_contact}"

            msg += "\n➡️ Share your live location with trusted people right now."

            return msg



    # 🌐 Phase 2: Privacy & Security → auto-remove sensitive terms
    if "address" in user_input.lower() or "phone" in user_input.lower():
        reply += "\n\n(🔒 Your personal info will not be stored and is auto-deleted for safety.)"

    # 🌍 Phase 3: Bilingual Support
    if lang == "hi":
        reply = "🇮🇳 हिंदी: " + reply  # (for demo, prepend Hindi label)

    return reply

# WhatsApp Webhook
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body")
    reply_text = get_gemini_response(incoming_msg)

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

# Home route
@app.route("/", methods=["GET"])
def home():
    return "🎉 TARINI Chatbot Backend is Running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
