SYSTEM_PROMPT = """You are a calm, laser-focused, point-scoring academic triage coach (Panic2Pass AI).
Your purpose is to maximize exam marks under extreme time pressure.
- Prioritize core formulas, definitions, mechanisms, and common exam traps.
- Use clear markdown structure, bullet points, and bold text.
- Avoid unnecessary introductory filler; jump straight into high-yield content.
"""

def generate_prompt(mode: str, context: str, weak_topic: str) -> str:
    topic = weak_topic.strip() if weak_topic and weak_topic.strip() else "Core high-yield concepts in these notes"

    if mode == "🆘 I'm Lost (Explain Simply)":
        return f"""Context Notes:
{context}

Confusing Focus Area: '{topic}'

Task: Demystify this concept for a panicking student:
1. 💡 **Core Intuition in 2 Sentences**: What problem does this actually solve in simple English?
2. 🚗 **1 Memorable Real-World Analogy**: Relate it to everyday life.
3. 🧩 **Step-by-Step Breakdown**: 3 numbered, jargon-free steps explaining how it works.
4. ⚠️ **The #1 Exam Trap**: The most common mistake or misconception students make.
"""

    elif mode == "📝 Quiz Me (High Yield)":
        return f"""Context Notes:
{context}

Target Topic: '{topic}'

Task: Generate 3 high-probability exam questions:
- **Question 1 (Definition / Concept Check - 2 Marks)**
- **Question 2 (Core Mechanism / Application - 5 Marks)**
- **Question 3 (Common Scenario / Edge Case - 5 Marks)**

Under each question, provide a brief hint, followed by the complete, crystal-clear **Model Answer** that examiners look for.
"""

    elif mode == "📋 Rapid Cheat Sheet":
        return f"""Context Notes:
{context}

Target Focus: '{topic}'

Task: Generate a high-retention Cheat Sheet:
1. 📌 **Key Terms & Definitions Matrix** (Table: Term | Plain English Meaning | Formula/Rule)
2. ⚙️ **Core Steps / Workflow Algorithm** (Clean numbered sequence)
3. 🚫 **Common Pitfalls & Exam Traps Checklist**
"""

    else:  # "⚡ 30-Min Crash Plan"
        return f"""Context Notes:
{context}

Exam in 30 minutes! Target Topic: '{topic}'

Task: Create a high-intensity 30-minute exam rescue schedule:
- ⏱️ **First 10 mins (Definitions & Formulas)**: Top 3 must-know definitions/formulas with immediate takeaway.
- ⏱️ **Next 15 mins (Core Mechanisms)**: The 2 most critical problem-solving steps or process diagrams.
- ⏱️ **Last 5 mins (Hall-Door Checklist)**: 3 quick memory triggers to glance at right outside the exam room.
"""
