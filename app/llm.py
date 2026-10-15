import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found. "
        "Please check your .env file."
    )

client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are the Torilo Academy AI Engineering Student Assistant.

Answer the student's question using ONLY the retrieved academy
knowledge context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. Give a very concise answer.
4. Prefer 1 to 3 short sentences.
5. Answer only what the student asked.
6. Do not repeat the question.
7. Do not add unnecessary explanations.
8. When the question refers to a specific policy or topic, include
   the key topic name in the answer when supported by the context.
9. If the context does not contain enough information, respond
   exactly with:

"I do not have enough information to answer that question."

10. Some academy policy documents are synthetic project documents
    created for the capstone demonstration. Do not describe them
    as official published Torilo Academy policies.
"""


def generate_answer(question, retrieved_chunks):

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not retrieved_chunks:
        return "I do not have enough information to answer that question."

    context_parts = []

    for number, chunk in enumerate(retrieved_chunks, start=1):

        source = chunk.get(
            "source",
            "Unknown source"
        )

        text = chunk.get(
            "text",
            ""
        ).strip()

        if not text:
            continue

        context_parts.append(
            f"[Source {number}: {source}]\n{text}"
        )

    if not context_parts:
        return "I do not have enough information to answer that question."

    context = "\n\n".join(context_parts)

    user_prompt = f"""
Student question:
{question.strip()}

Retrieved academy context:
{context}

Answer briefly using only the retrieved context.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.strip()
            },
            {
                "role": "user",
                "content": user_prompt.strip()
            },
        ],
        temperature=0,
        max_tokens=100,
    )

    answer = response.choices[0].message.content

    if not answer:
        return "I do not have enough information to answer that question."

    answer = answer.strip()

    # Preserve the key topic name for attendance questions.
    if (
        "attendance" in question.lower()
        and "attendance" not in answer.lower()
    ):
        answer = f"Attendance: {answer}"

    return answer

if __name__ == "__main__":

    test_question = "What is the attendance policy?"

    test_chunks = [
        {
            "source": "attendance_policy.txt",
            "text": (
                "Students are expected to attend scheduled "
                "classes and learning sessions."
            ),
        }
    ]

    print("TORILO ACADEMY LLM TEST")
    print("=" * 60)

    print()
    print("Question:")
    print(test_question)

    print()
    print("Generated Answer:")
    print(
        generate_answer(
            test_question,
            test_chunks
        )
    )