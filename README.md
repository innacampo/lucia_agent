# 1. LUCIA: A Collaborative Clinical Instrument
LUCIA is an AI-powered scientific instrument that analyzes medical research to surface and mitigate diagnostic bias in women's health.LUCIA (Language Understanding for Clinical Insight & Analysis) is a dual-agent platform designed as a bridge, not a wedge.
- For the Clinician (Efficiency & Safety): It acts as an intelligent "pre-screener," synthesizing complex narratives into structured clinical data before the patient even enters the room. It reduces cognitive load and serves as a safety net against burnout-induced errors.
- For the Researcher (Discovery & Equity): The "AXIOM Engine" concept aims to repair the foundation of medical knowledge. While simulated for this capstone, the architectural vision is to bridge research gaps by scanning PubMed via MCP to flag systemic bias in literature and collect patient narratives to fill medical "Data Voids" with real-world evidence.

## **Setup**

# 2. Why Agents?
LUCIA utilizes a Multi-Agent Architecture to solve this:
- **Specialization:** By assigning distinct roles (Symptom Mapper vs. Bias Analyzer), we ensure a rigorous separation between the patient's own thoughts and existing clinical assumptions.
- **Statefulness:** Our agents maintain a dynamic "Session State" - a persistent memory object that evolves in real-time. It continuously updates the symptoms and detected biases based on patient input, ensuring the agent's reasoning adapts as the narrative unfolds.
- **Verifiable Tool Use:**  Agents can trigger specific tools (like the "AXIOM Knowledge Base") to ground their insights in peer-reviewed literature, rather than relying on the black-box training data of an LLM.

#3. Architecture & Workflow ("The Dual-Stream Engine")  
LUCIA is a Multi-Agent Orchestration built on the Google Agent Development Kit (ADK). The system processes the patient's subjective narrative through four distinct stages to create a structured clinical asset.
1. Ingest & Map: The Digital Scribe
Agent 1  `symptom_mapper`: Acting as a scribe for overloaded clinicians, this agent ingests the user's narrative and translates emotional history into a structured Review of Systems (ROS).
Action: It updates the `symptomMapping` state in memory (e.g., mapping "brain fog" to neurological clusters), allowing the doctor to skip data entry and focus on diagnosis.
2. Audit: Clinical Decision Support
Agent 2 `bias_analyzer` : Acting as a non-judgmental "second opinion," this agent audits the narrative for cognitive traps like premature closure or attribute substitution.
Tool  `get_bias_implications` : The agent queries the AXIOM Engine, a validated dictionary of bias implications, to ground its insights in external, controlled facts rather than LLM weights.
Action: It asynchronously updates the `biasAwareness state`, framing potential biases not as errors, but as diagnostic pivot points. 
3. Advocacy: The Patient Prep Engine
Agent 3 (`advocacy_generator`): Recognizing that a prepared patient is a partner, this agent transforms anxiety into a structured agenda.
Action: Based on the `symptomMapping` and `biasAwareness` states, it generates `structuredAdvocacy` - a list of differential diagnosis requests (e.g., "Given symptoms X and Y, should we check thyroid function?") - to focus the conversation on clinical investigation.
4. Structure: The Clinical Handoff
Agent 4 (`report_formatter`): This agent compiles the final output into a professional Consultation Brief.
Action: It generates the final report using a standard medical note layout (Subjective -> Assessment  -> Plan), ensuring the output is instantly scannable for the provider and positions the patient and doctor on the same side of the table.
# 4. Demo Scenario: The "Perimenopause" Dismissal
In this scenario, a 48-year-old user shares a frustrating interaction regarding autoimmune-like symptoms.

##Step 1: The Narrative (Input)  
*User:* "I've been waking up with stiff, swollen joints in my hands and feet for three months. The fatigue is so bad I have to nap in my car at lunch. I saw a new doctor today. I tried to show him the swelling, but he barely looked. He told me that at 48, this is just classic perimenopause and 'empty nest syndrome' making me depressed. He didn't order any blood work. He just told me to lose 10 pounds and try meditation to calm my 'nerves' because women get so anxious at this stage of life."

##Step 2: The Logic (Internal Monologue & Tool Usage)   
Agent 1 (Symptom Mapper): Extracts Symptoms and assigns them to clusters:
stiff joints in my hands and feet  -> pain cluster
fatigue  -> fatigue cluster
swollen joints in my hands and feet  -> musculoskeletal cluster
Agent 2 (Bias Analyzer): Detects bias markers in the narrative (attribution of physical swelling to 'nerves') and queries the AXIOM Knowledge Base.
Tool Call: `get_bias_implications(bias_type="ageism_bias")`
Output: "Dismissing a patient's medical concerns as a normal or inevitable part of aging. This can prevent the timely diagnosis and treatment of serious conditions like heart disease, cancer, or neurological issues."
Tool Call: `get_bias_implications(bias_type="gender_bias")`
Output: "Often results in women's pain being taken less seriously or misdiagnosed, particularly in cardiovascular and autoimmune diseases."

##Step 3: The Output (Advocacy Report)  
LUCIA generates the following document for the patient:
**Patient Advocacy & Consultation Aid**

**Disclaimer:** This report is generated to assist in patient–doctor communication and is not medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.

**1. Summary of Reported Symptoms:**
* Pain Cluster: stiff joints in my hands and feet
* Fatigue Cluster: fatigue
* Musculoskeletal Cluster: swollen joints in my hands and feet

**2. Communication & Bias Insights:**
* Ageism Bias
    * Observation: Doctor attributed joint swelling, stiffness, and fatigue to perimenopause and 'empty nest syndrome' at age 48 without ordering tests.
    * Potential Risk: Dismissing a patient's medical concerns as a normal or inevitable part of aging. This can prevent the timely diagnosis and treatment of serious conditions like heart disease, cancer, or neurological issues.
* Gender Bias
    * Observation: Doctor attributed symptoms to 'empty nest syndrome' and anxiety due to the patient's age and sex, and suggested weight loss and meditation instead of medical investigation.
    * Potential Risk: Often results in women's pain being taken less seriously or misdiagnosed, particularly in cardiovascular and autoimmune diseases.

**3. Suggested Questions for Your Doctor:**
* What further evaluations could help understand my stiff and swollen joints?
* Are there additional causes for my fatigue we should consider?
* Could we explore explanations for my symptoms beyond age-related changes?
* How can we ensure my symptoms are evaluated thoroughly, considering potential gender-related factors in diagnosis?
  
# 5. The Build
This project was built using the Google Agent Development Kit (ADK) and Gemini 2.5 Flash.
The architecture leverages the following ADK components:
**Multi-agent System**
- Agent powered by an LLM: We utilized LlmAgent for the four core specialized workers: `symptom_mapper_agent`, `bias_analyzer_agent`, `advocacy_generator_agent`, and `report_formatter_agent`.
- Parallel Agents: The ParallelAgent primitive (`parallel_analysis_step`) is used to run the Symptom Mapper and Bias Analyzer simultaneously. This reduces latency by processing the patient's narrative for both clinical signs and bias markers at the same time.
- Sequential Agents:  The SequentialAgent primitive (`analysis_workflow_agent`) orchestrates the final pipeline, ensuring that the advocacy and reporting steps only trigger after the parallel analysis is complete.

**Tools**
- Custom Tools: We implemented a custom Python function tool, `get_bias_implications`. In this prototype, it acts as a mock interface for the AXIOM Engine, retrieving validated clinical context from a static dictionary to ground the Bias Analyzer's output.

**Sessions & Memory**
- Sessions & State Management: We utilized `InMemorySessionService` to maintain the conversation state. The agents share a structured context object, passing JSON data (keys like `symptomMapping` and `biasAwareness`) between steps without losing the patient's original narrative.

The most significant challenge for me was managing the intricate dependency between agent orchestration and prompt engineering. While the ADK provided the architectural scaffolding for parallel and sequential flows, I discovered that structural orchestration and prompt design must go hand-in-hand. It was not enough to simply connect the agents; I had to rigorously iterate on the system instructions to ensure strict "role scoping." A major challenge was preventing context leakage, where agents might attempt to perform tasks outside their domain. By refining the prompts to enforce specific JSON output schemas and behavioral constraints, I strove to ensure that every agent precisely understood its isolated role within the broader pipeline.

# 6. **Cloud Deployment (Vertex AI Agent Engine)**

The LUCIA agent has been successfully deployed to Google Cloud's Vertex AI Agent Engine. It is operational as a secure, serverless API.

* **Platform:** `Vertex AI Agent Engine`
* **Region:** `us-central1`
* **Endpoint Resource Name:** `available upon request`
  *This endpoint is secured via Google Cloud IAM. Access is granted programmatically via authenticated requests, as demonstrated in the deployment notebook. https://www.kaggle.com/code/innacampo/lucia-agent-deployment*

### **Deployment Artifacts**

`lucia_deploy/`
`├── agent.py                  # The logic`
`├── requirements.txt          # The libraries`
`├── .env                      # The secrets/config`
`└── .agent_engine_config.json # The hardware specs`

### **Deploy Command**

`adk deploy agent_engine --project=$PROJECT_ID --region=$deployed_region lucia_deploy --agent_engine_config_file=lucia_deploy/.agent_engine_config.json`

# 7. Future Vision
This capstone demonstrates LUCIA's immediate utility, but its long-term value lies in longitudinal observation.
For Researchers: Future iterations will allow women to donate anonymized data to AXIOM, creating the "Big Data" needed to update guidelines. This feature is deferred in this prototype to prioritize strict PHI/HIPAA governance.
For Clinicians: It provides a "longitudinal view" of a patient's journey, revealing cyclical patterns invisible in snapshot appointments.
LUCIA is more than code, it is a proof of concept for a healthcare system that listens.
