TORILO ACADEMY AI ENGINEERING STUDENT ASSISTANT
CAPSTONE EVALUATION REPORT

============================================================
1. PROJECT OVERVIEW
============================================================

The Torilo Academy AI Engineering Student Assistant is an
AI-powered student support chatbot designed to answer questions
using an approved academy knowledge base and structured course
information.

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

The system is designed to avoid inventing information that is
not contained in the available academy knowledge base.

Some knowledge-base documents contain synthetic project
information created specifically for the capstone demonstration.
Such information is clearly identified and should be replaced
with verified Torilo Academy information before production use.


============================================================
2. SYSTEM ARCHITECTURE
============================================================

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
Short Conversation Memory
       |
       v
Context Resolver
       |
       v
Question Router
       |
       +-------------------------+
       |                         |
       v                         v
Structured Question       Knowledge Question
       |                         |
       v                         v
SQLite Database                 RAG
       |                         |
       |                         v
       |                    Retriever
       |                         |
       |                         v
       |                    Vector Store
       |                         |
       |                         v
       |                        LLM
       |                         |
       +-----------+-------------+
                   |
                   v
             Final Answer
                   |
                   v
           Source Attribution
                   |
                   v
           Gradio Interface

The context resolver operates before routing so that simple
follow-up questions can be converted into complete questions.

The system also contains an unknown/out-of-scope route that
returns a safe response when the question is outside the
available knowledge domains.


============================================================
3. KNOWLEDGE BASE
============================================================

The chatbot uses academy project documents stored in:

data/documents/

The final knowledge base contains 16 documents:

1. assessment_policy.txt
2. attendance_policy.txt
3. course_catalog.txt
4. faq.txt
5. learning_procedures.txt
6. payment_policy.txt
7. refund_policy.txt
8. student_conduct_policy.txt
9. student_handbook.txt
10. student_policy.txt
11. support_procedures.txt
12. academy_overview.txt
13. ai_engineering_programme.txt
14. enrollment_requirements.txt
15. product_management.txt
16. student_support.txt

The knowledge base covers:

- Academy information
- Courses
- AI Engineering
- Product Management
- Enrollment requirements
- Student support
- Student handbook
- Attendance
- Assessment
- Payment
- Refunds
- Student conduct
- Learning procedures
- Student policies
- Support procedures
- Frequently asked questions

The course catalog contains 14 structured academy courses with
their categories, durations and fees.

The five additional documents added during the final capstone
development stage provide academy overview, AI Engineering,
Product Management, enrollment and student-support information.

Some of these additional documents contain synthetic project
information and are clearly marked as such.


============================================================
4. STRUCTURED COURSE DATABASE
============================================================

Course information is also stored in SQLite:

data/database/torilo_academy.db

The database contains:

- Course name
- Category
- Duration in weeks
- Course fee

The chatbot routes structured course questions directly to
SQLite.

Examples include:

- Course fee questions
- Course duration questions
- Course category questions

This allows deterministic retrieval of structured course
information without requiring an LLM call.

The structured database contains 14 courses.


============================================================
5. RETRIEVAL-AUGMENTED GENERATION
============================================================

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

Embedding dimension:

384

The final vector store contains:

55 embedded chunks

The current chatbot retrieves:

top_k = 3

relevant chunks for knowledge questions.

A small source-priority adjustment is used for course/category
retrieval so that the authoritative course catalog is preferred
for course-category questions.


============================================================
6. CONVERSATION MEMORY AND CONTEXT RESOLUTION
============================================================

The chatbot maintains a short conversation history.

Current configuration:

max_memory_turns = 3

This limits the amount of previous conversation retained by the
chatbot.

The system also contains a context resolver that handles simple
follow-up questions.

Example:

First question:

"How much is Software Engineering?"

Follow-up:

"How long is it?"

The context resolver converts the follow-up into:

"How long is Software Engineering/Development?"

The resolved question is then routed to the structured database.

The context resolver also supports follow-up questions involving
programmes such as Product Management and AI Engineering.


============================================================
7. SOURCE ATTRIBUTION
============================================================

The chatbot displays the source associated with the answer.

For structured course questions, the source can be:

Torilo Academy course database

For RAG questions, the source can be a specific document, such
as:

attendance_policy.txt

Source attribution improves transparency by showing where the
information used for the response came from.


============================================================
8. LLM RESPONSE GENERATION
============================================================

The chatbot uses the LLM:

gpt-4o-mini

The LLM is instructed to:

- Use only retrieved academy context
- Avoid inventing information
- Provide concise answers
- Generally answer in 1 to 3 short sentences
- Return a safe response when sufficient information is not
  available

The standard safe response for unsupported questions is:

"I do not have enough information to answer that question."

The LLM temperature is configured for deterministic behaviour.


============================================================
9. GRADIO INTERFACE
============================================================

The chatbot has a Gradio web interface.

The local application runs at:

http://127.0.0.1:7860

The interface supports:

- Student questions
- Conversation history
- Follow-up questions
- Answer generation
- Source display

The Gradio implementation uses session-isolated state so that
conversation memory is maintained separately for each user
session rather than being shared globally across users.

The RAG interface configuration uses:

top_k = 3

and:

max_memory_turns = 3


============================================================
10. LIVE GRADIO TESTING
============================================================

The live chatbot was tested using representative student
questions.

### Test 1 — Course Fee

Question:

"How much is Software Engineering?"

Expected information:

Software Engineering/Development — ₦250,000

Source:

Torilo Academy course database

Result:

PASS


### Test 2 — RAG Knowledge Question

Question:

"What is the attendance policy?"

Result:

The chatbot returned information concerning attendance and
notification procedures.

Source:

attendance_policy.txt

Result:

PASS


### Test 3 — Conversation Follow-up

Initial question:

"How much is Software Engineering?"

Follow-up:

"How long is it?"

Result:

Software Engineering/Development has a duration of 12 weeks.

Source:

Torilo Academy course database

Result:

PASS


============================================================
11. FINAL 20-QUESTION LIVE EVALUATION
============================================================

A final live evaluation was performed using 20 representative
student questions covering academy information, programmes,
policies, support, follow-up questions and unknown information.

The evaluation included questions about:

1. Torilo Academy
2. Available courses
3. AI Engineering duration
4. AI Engineering topics
5. Product Management learning formats
6. Enrollment requirements
7. Attendance policy
8. Refund policy
9. Student Support
10. Academy campuses
11. Missing a class
12. Suitable programme for AI interests
13. Suitable programme for product management interests
14. Remote/online learning
15. Product Management follow-up
16. Attendance follow-up
17. Abuja campus
18. Student accommodation
19. Next AI Engineering cohort date
20. Current President

Final result:

20/20 LIVE TESTS PASSED


============================================================
12. UNKNOWN AND OUT-OF-SCOPE HANDLING
============================================================

The chatbot is designed not to invent answers when information
is outside the available knowledge base.

For unsupported questions, the chatbot returns:

"I do not have enough information to answer that question."

The final evaluation included questions for which the knowledge
base did not contain sufficient information.

Examples included:

- Whether Torilo Academy has an Abuja campus
- Whether student accommodation is provided
- The exact date of the next AI Engineering cohort
- The identity of the current President

The chatbot safely avoided inventing unsupported information.

This behaviour is an important part of the system's reliability
design.


============================================================
13. SYNTHETIC PROJECT INFORMATION
============================================================

Some documents contain synthetic information created for the
capstone demonstration because verified institutional
information was not supplied.

Synthetic information is clearly identified within the relevant
documents.

Examples include information relating to:

- Enrollment requirements
- Student Support procedures
- AI Engineering programme details
- Product Management programme details
- Academy overview information

Synthetic information must not be presented as verified official
Torilo Academy information.

Before production deployment, the synthetic information should
be replaced with verified information supplied by Torilo Academy.


============================================================
14. TOKEN-EFFICIENCY DESIGN
============================================================

Token usage was considered during system design.

The following techniques are used:

### 14.1 Structured Questions Bypass the LLM

Course fee, duration and category questions are handled directly
by SQLite.

This avoids unnecessary LLM calls.

### 14.2 Limited Retrieval

The RAG system currently retrieves only:

top_k = 3

This prevents unnecessary document chunks from being sent to the
LLM.

### 14.3 Short Conversation Memory

The system retains only:

3 conversation turns

This prevents unnecessary historical conversation from growing
indefinitely.

### 14.4 Concise LLM Responses

The LLM is instructed to provide concise answers, generally using
1 to 3 short sentences.

### 14.5 Unknown Questions Avoid the LLM

Unknown questions are handled directly by the application instead
of unnecessarily sending them to the LLM.

These design choices reduce unnecessary computation and LLM token
usage while maintaining answer quality.


============================================================
15. AUTOMATED EVALUATION
============================================================

A formal capstone evaluation suite was created in:

tests/test_capstone_evaluation.py

The dedicated capstone evaluation suite contains 10 tests.

The complete project test suite contains:

74 automated tests

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

Final dedicated capstone evaluation:

10/10 PASSED

Final complete project regression:

74/74 PASSED

Latest full regression execution time:

375.26 seconds


============================================================
16. AUTOMATED EVALUATION RESULTS
============================================================

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

Overall automated result:

74/74 PASS


============================================================
17. RETRIEVAL EVALUATION
============================================================

The retriever was evaluated using representative knowledge
questions.

The retrieval tests covered topics including:

- Academy overview
- AI Engineering duration
- AI Engineering topics
- Enrollment requirements
- Product Management learning formats
- Student Support
- Academy campuses
- Course categories

The final retrieval system correctly identified relevant
knowledge-base sources for the evaluated questions.

The automated retriever tests passed successfully as part of the
complete 74-test regression suite.


============================================================
18. RELIABILITY OBSERVATIONS
============================================================

The evaluation demonstrates that the system can successfully:

- Route structured questions to SQLite
- Route knowledge questions to RAG
- Retrieve relevant academy information
- Generate concise answers from retrieved context
- Resolve simple conversational follow-ups
- Maintain a limited conversation history
- Provide source information
- Reject unsupported questions safely
- Handle programme-specific questions
- Handle academy overview questions
- Handle enrollment and student-support questions

The evaluation does not establish that every possible user
question will be answered correctly.

The tests cover representative functionality rather than
exhaustive language coverage.


============================================================
19. CURRENT PROJECT LIMITATIONS
============================================================

### 19.1 Limited Query Routing

The router currently relies primarily on predefined keywords and
patterns.

More complex natural-language variations may require additional
routing logic.

### 19.2 Limited Context Resolution

The context resolver currently handles a defined set of follow-up
question patterns.

More complex references may require additional context-resolution
logic.

### 19.3 Synthetic Information

Some academy information is synthetic project information created
for the capstone demonstration.

It should be replaced with verified institutional information
before production use.

### 19.4 Local Deployment

The current Gradio application is running locally rather than as
a publicly deployed production service.

### 19.5 Knowledge-Base Maintenance

The academy knowledge base must be updated when official course,
programme, policy or support information changes.

The chatbot should not be considered a permanent source of
institutional information without a controlled knowledge-base
update process.


============================================================
20. FINAL PROJECT ARCHITECTURE
============================================================

The final architecture consists of:

User Interface:
Gradio

Application Layer:
ToriloAcademyChatbot

Conversation Layer:
Short-term Conversation Memory
Context Resolver

Decision Layer:
Question Router

Structured Knowledge Layer:
SQLite Course Database

Unstructured Knowledge Layer:
16 Academy Documents

Retrieval Layer:
Sentence-Transformer Embeddings
Vector Store
Cosine Similarity Retriever

Generation Layer:
gpt-4o-mini

Safety Layer:
Grounded Responses
Unknown-Question Handling
Out-of-Scope Handling
Synthetic-Information Labelling

Testing Layer:
Pytest
Automated Regression Tests
Live Gradio Evaluation


============================================================
21. CAPSTONE DEMONSTRATION FLOW
============================================================

For a live project demonstration, the recommended sequence is:

1. Ask:

"How much is Software Engineering?"

Demonstrates:

Structured database retrieval


2. Ask:

"How long is it?"

Demonstrates:

Conversation memory
Context resolution
Structured retrieval


3. Ask:

"What is the attendance policy?"

Demonstrates:

Question routing
RAG
Source attribution


4. Ask:

"What is the refund policy?"

Demonstrates:

Knowledge retrieval


5. Ask:

"What is today's weather?"

Demonstrates:

Unknown/out-of-scope handling


6. Ask:

"What is the AI Engineering programme?"

Demonstrates:

Programme-specific knowledge retrieval


7. Ask:

"What learning formats are available for Product Management?"

Demonstrates:

Programme-specific RAG retrieval


8. Ask:

"How can I contact Student Support?"

Demonstrates:

Student Support knowledge retrieval and safe handling of
missing official contact details.


============================================================
22. FINAL EVALUATION CONCLUSION
============================================================

The Torilo Academy AI Engineering Student Assistant successfully
demonstrates an end-to-end AI engineering workflow combining:

- Structured data retrieval
- Retrieval-Augmented Generation
- Document processing
- Text cleaning
- Text chunking
- Sentence-transformer embeddings
- Vector search
- LLM generation
- Query routing
- Conversation memory
- Context resolution
- Source attribution
- Unknown-question handling
- Gradio interface
- Automated testing
- Live evaluation

The final automated regression result is:

74/74 TESTS PASSED

The dedicated capstone evaluation result is:

10/10 TESTS PASSED

The final live evaluation result is:

20/20 TESTS PASSED

The project therefore demonstrates a functional AI Engineering
student-assistant chatbot suitable for capstone demonstration,
with clear limitations and a defined path toward production
readiness.


============================================================
23. FINAL PROJECT STATUS
============================================================

Project:

Torilo Academy AI Engineering Student Assistant

Knowledge Base:

16 documents

Vector Store:

55 embedded chunks

Embedding Model:

all-MiniLM-L6-v2

Embedding Dimension:

384

Structured Database:

SQLite

LLM:

gpt-4o-mini

RAG Retrieval:

top_k = 3

Conversation Memory:

3 turns

Automated Evaluation:

74/74 PASS

Dedicated Capstone Evaluation:

10/10 PASS

Final Live Evaluation:

20/20 PASS

Live Interface:

Successfully running locally

Overall Development Status:

CAPSTONE FUNCTIONALITY VERIFIED

============================================================
END OF CAPSTONE EVALUATION REPORT
============================================================  