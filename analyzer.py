import google.generativeai as genai
from groq import Groq
from config import GEMINI_API_KEY, GROQ_API_KEY, GEMINI_MODEL, GROQ_MODEL

genai.configure(api_key=GEMINI_API_KEY)


# ── Format helper ─────────────────────────────────────
def _format(reviews):
    lines = []
    for i, r in enumerate(reviews, 1):
        lines.append(
            f"[{i}] Source: {r['source']}\n"
            f"    Title  : {r['title']}\n"
            f"    Content: {r['snippet']}\n"
            + "─" * 50
        )
    return "\n".join(lines)


# ── Gemini Analysis ───────────────────────────────────
def analyze_with_gemini(product, reviews_text):
    try:
        model  = genai.GenerativeModel(GEMINI_MODEL)
        prompt = f"""
You are a highly critical and expert product analyst. Analyze these reviews for "{product}" and give a brutally honest detailed report.
You MUST highlight the product's shortcomings, flaws, and negative points clearly.

REVIEWS:
{reviews_text}

Respond in this exact format:
### ⭐ FINAL RATING: [X/10]

### ⚠️ CRITICAL FLAWS & SHORTCOMINGS (Kamiyan)
- (Detailed bullet points of all negative aspects)

### ✅ PROS & BENEFITS
- (Detailed bullet points)

### 💬 SENTIMENT & RECOMMENDATION
- **Sentiment:** (Positive / Negative / Mixed)
- **Recommendation:** (Buy / Avoid / Consider — with reason)

### 📝 FINAL VERDICT
(2-3 sentences summarizing whether it is worth buying despite its flaws)
"""
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Gemini analysis failed → {e}"


# ── Groq Analysis ─────────────────────────────────────
def analyze_with_groq(product, reviews_text):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""Analyze these reviews for "{product}":

{reviews_text}

Give a FAST, CONCISE, and brutally honest response focusing heavily on the product's flaws.
Use this format:
### ⭐ FINAL RATING: [X/10]
### ⚠️ MAJOR SHORTCOMINGS (Kamiyan):
- (List the top flaws)
### ✅ TOP PROS:
- (List the best features)
### ⚖️ ONE-LINE VERDICT:"""

        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a highly critical, sharp product review analyst who finds flaws."},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=600,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Groq analysis failed → {e}"


# ── Marketing Content Generation ──────────────────────
def generate_marketing_content(product):
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        prompt = f"""
You are an expert digital marketer and AI prompt engineer.
Generate a comprehensive marketing package for the product "{product}".

Provide the output strictly in the following format:

### 📢 Short Ad Copy
(Generate a short, catchy, engaging, and social-media friendly advertisement paragraph. Tone: modern and persuasive.)

### 🪝 Marketing Hooks
(Generate 3 unique, attention-grabbing hooks suitable for Instagram, YouTube Shorts, Facebook, or LinkedIn. Format as a numbered list.)

### 🎨 AI Image Prompt
(Generate ONE highly detailed, cinematic prompt for Midjourney/DALL-E. Include lighting, camera angle, environment, colors, and realistic details.)

### 🎥 AI Video Ad Prompts
(Generate 3 cinematic AI video ad prompts for Runway/Sora/Kling. For each, describe scene setup, camera movement, lighting, product focus, background, emotional tone, and cinematic effects. Format as a numbered list.)
"""
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Marketing generation failed → {e}"


# ── Master Analyzer ───────────────────────────────────
def generate_final_review(product, reviews):
    if not reviews:
        return {"error": "No reviews collected. Check your API keys."}

    reviews_text = _format(reviews)

    print("\n🤖  AI Analysis in progress …\n")

    print("  ✨  Gemini analyzing …")
    gemini_result = analyze_with_gemini(product, reviews_text)

    print("  ⚡  Groq analyzing …")
    groq_result = analyze_with_groq(product, reviews_text)

    print("  🚀  Generating Marketing Content …")
    marketing_result = generate_marketing_content(product)

    return {
        "product":                product,
        "total_reviews_analyzed": len(reviews),
        "sources":                sorted(set(r["source"] for r in reviews)),
        "gemini_analysis":        gemini_result,
        "groq_analysis":          groq_result,
        "marketing_content":      marketing_result,
        "links":                  [r["link"] for r in reviews if r.get("link")][:6],
    }