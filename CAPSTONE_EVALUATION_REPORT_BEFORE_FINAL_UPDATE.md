Torilo Academy AI Engineering Student Assistant
# Capstone Evaluation Report
## 1. Project Overview
The Torilo Academy AI Engineering Student Assistant is an AI-powered
student support chatbot designed to answer questions using an approved
academy knowledge base and structured course information.
The system combines:
- Document-based Retrieval-Augmented Generation (RAG)
- SQLite structured data retrieval
- Query routing
- Sentence-transformer embeddings
- Vector similarity retrieval
- Large Language Model (LLM) response generation
- Conversation memory
- Follow-up question resolution
- Source attribution
- Gradio web interface
The system is designed to avoid inventing information that is not
contained in the academy knowledge base.
---
## 2. System Architecture
The major processing flow is:
Student Question
        |
        v
Gradio Interface
        |
        v
ToriloAcademyChatbot
        |
        v
Question Router
        |
        +--------------------+
        |                    |
        v                    v
Structured Question     Knowledge Question
        |                    |
        v                    v
SQLite Database             RAG
                             |
                             v
                         Retriever
                             |
                             v
                       Vector Store
                             |
                             v
                            LLM
        |                    |
        +---------+----------+
                  |
                  v
             Final Answer
                  |
                  v
             Source Display
                  |
                  v
          Gradio Interface
Conversation memory and context resolution operate before routing
to support follow-up questions.
---
## 3. Knowledge Sources
The chatbot uses academy project documents stored in:
data/documents/
The knowledge base contains documents covering areas such as:
- Course catalog
- Student handbook
- Attendance policy
- Assessment policy
- Payment policy
- Refund policy
- Student conduct policy
- Learning procedures
- Support procedures
- FAQ
- Student policy
The course catalog contains 14 academy courses with their
categories, durations, and fees.
---
## 4. Structured Course Database
Course information is also stored in SQLite:
data/database/torilo_academy.db
The database contains:
- Course name
- Category
- Duration in weeks
- Course fee
The chatbot routes structured course questions directly to SQLite.
Examples include:
- Course fee questions
- Course duration questions
- Course category questions
This allows deterministic retrieval of structured information
without requiring an LLM call.
---
## 5. Retrieval-Augmented Generation
Knowledge-based questions are handled through the RAG pipeline.
The pipeline consists of:
1. Document loading
2. Text cleaning
3. Document chunking
4. Embedding generation
5. Vector-store creation
6. Query embedding
7. Cosine-similarity retrieval
8. Relevant context selection
9. LLM answer generation
The embedding model used is:
all-MiniLM-L6-v2
The vector embeddings contain 384 dimensions.
The current chatbot retrieves:
top_k = 3
relevant chunks for knowledge questions.
---
## 6. Conversation Memory
The chatbot maintains a short conversation history.
The current configuration is:
max_memory_turns = 3
This limits the amount of previous conversation retained by the
chatbot.
The system also contains a context resolver that handles simple
follow-up questions.
For example:
First question:
"How much is Software Engineering?"
Follow-up:
"How long is it?"
The context resolver converts the follow-up into:
"How long is Software Engineering/Development?"
The resolved question is then routed to the structured database.
---
## 7. Source Attribution
The chatbot displays the source associated with the answer.
For structured course questions, the source can be:
Torilo Academy course database
For RAG questions, the source can be a specific document, such as:
attendance_policy.txt
This improves transparency by showing where the information used
for the response came from.
---
## 8. Gradio Interface Testing
The chatbot was successfully launched using Gradio.
Local application URL:
http://127.0.0.1:7860
The following live interface tests were successfully performed:
### Test 1 — Course Fee
Question:
"How much is Software Engineering?"
Result:
"The fee for Software Engineering/Development is ₦250,000."
Source:
Torilo Academy course database
Result: PASS
---
### Test 2 — RAG Knowledge Question
Question:
"What is the attendance policy?"
Result:
The chatbot returned information concerning attendance and
notification procedures.
Source:
attendance_policy.txt
Result: PASS
---
### Test 3 — Conversation Follow-up
Initial question:
"How much is Software Engineering?"
Follow-up:
"How long is it?"
Result:
"Software Engineering/Development has a duration of 12 weeks."
Source:
Torilo Academy course database
Result: PASS
---
## 9. Automated Evaluation
A formal capstone evaluation suite was created in:
tests/test_capstone_evaluation.py
The capstone evaluation suite contains 10 dedicated automated tests, and the complete project test suite contains 74 automated tests.
The evaluation covers:
1. Course fee accuracy
2. Course duration accuracy
3. Category accuracy
4. RAG routing
5. Source attribution
6. Follow-up context resolution
7. Unknown-question safety
8. Out-of-scope question safety
9. Conversation-memory limit
10. Complete conversation flow
Final capstone evaluation result:
10 passed in the dedicated capstone evaluation suite.
Complete project test-suite result:
74 passed in 691.81 seconds (0:11:31)
Overall result:
74/74 tests passed
---
## 10. Evaluation Results
| Evaluation Area | Result |
|---|---|
| Course fee accuracy | PASS |
| Course duration accuracy | PASS |
| Category accuracy | PASS |
| RAG routing | PASS |
| Source attribution | PASS |
| Follow-up/context resolution | PASS |
| Unknown-question safety | PASS |
| Out-of-scope safety | PASS |
| Conversation-memory limit | PASS |
| Complete conversation flow | PASS |
Final result:
74/74 PASS
---
## 11. Unknown and Out-of-Scope Handling
The chatbot is designed not to invent answers when information is
outside the available knowledge base.
For unsupported questions, the chatbot returns:
"I do not have enough information to answer that question."
This behavior was tested using questions such as:
"What is the weather in Lagos today?"
and:
"Who is the president of Nigeria?"
Both were correctly classified as unknown/out-of-scope questions.
---
## 12. Token-Efficiency Design
Token usage was considered during system design.
The following techniques are used:
### 12.1 Structured Questions Bypass the LLM
Course fee, duration, and category questions are handled directly
by SQLite.
This avoids unnecessary LLM calls.
### 12.2 Limited Retrieval
The RAG system currently retrieves only:
top_k = 3
This prevents unnecessary document chunks from being sent to the LLM.
### 12.3 Short Conversation Memory
The system retains only:
3 conversation turns
This prevents unnecessary historical conversation from growing
indefinitely.
### 12.4 Concise LLM Responses
The LLM is instructed to provide concise answers, generally using
1 to 3 short sentences.
### 12.5 Unknown Questions Avoid the LLM
Unknown questions are handled directly by the application instead
of unnecessarily sending them to the LLM.
---
## 13. Reliability Observations
The evaluation demonstrates that the system can successfully:
- Route structured questions to SQLite
- Route knowledge questions to RAG
- Retrieve relevant academy information
- Generate concise answers from retrieved context
- Resolve simple conversational follow-ups
- Maintain a limited conversation history
- Provide source information
- Reject unsupported questions safely
The evaluation does not establish that every possible user question
will be answered correctly. The tests cover representative
functionality rather than exhaustive language coverage.
---
## 14. Current Project Limitations
The current implementation has several limitations.
### 14.1 Limited Query Routing
The router currently relies primarily on predefined keywords and
patterns.
More complex natural-language variations may require additional
routing logic.
### 14.2 Limited Context Resolution
The context resolver currently handles a defined set of follow-up
question patterns.
More complex references may require additional context-resolution
logic.
### 14.3 Synthetic Policy Documents
Some academy policy documents are synthetic project documents
created for the capstone demonstration.
They should not be presented as verified official published
Torilo Academy policies.
### 14.4 Local Deployment
The current Gradio application is running locally rather than as
a publicly deployed production service.
### 14.5 Multi-User Session Isolation
The current Gradio implementation creates one chatbot instance
for the application.
For a production multi-user deployment, conversation memory should
be isolated per user/session.
---
## 15. Final Evaluation Conclusion
The Torilo Academy AI Engineering Student Assistant successfully
passed the formal capstone evaluation suite.
Final automated result:
74/74 tests passed in the complete project test suite.
The live Gradio interface was also successfully tested with:
- Structured course questions
- RAG knowledge questions
- Conversation follow-up questions
- Source attribution
The project therefore demonstrates an end-to-end AI engineering
workflow combining structured data retrieval, RAG, embeddings,
vector search, LLM generation, conversation memory, context
resolution, routing, testing, and a web-based user interface.
---
## 16. Capstone Demonstration Flow
For a live project demonstration, the recommended sequence is:
1. Ask:
   "How much is Software Engineering?"
2. Ask:
   "How long is it?"
3. Ask:
   "What is the attendance policy?"
4. Ask:
   "What is the refund policy?"
5. Ask an unsupported question:
   "What is today's weather?"
6. Show the corresponding source displayed with each answer.
This demonstrates:
- Structured retrieval
- Conversation memory
- Context resolution
- RAG
- Source attribution
- Safe unknown handling
---
## 17. Final Project Status
Project:
Torilo Academy AI Engineering Student Assistant
Architecture:
Structured Database + RAG + LLM + Conversation Memory + Gradio
Automated Evaluation:
74/74 PASS
Live Interface:
Successfully running locally
Overall Development Status:
CAPSTONE FUNCTIONALITY VERIFIED