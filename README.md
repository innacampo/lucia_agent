![Logo](./images/logo.png "LUCIA logo")
# LUCIA: Bias-Aware AI Agent

![Status](https://img.shields.io/badge/Status-Prototype-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Tech](https://img.shields.io/badge/Built%20With-Google%20ADK%20%7C%20Gemini%202.5-orange)
![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)

> **"A bridge, not a wedge."** - Closing the gender diagnostic gap with Multi-Agent Systems.

**LUCIA (Language Understanding for Clinical Insight & Analysis)** is a dual-agent AI instrument designed to address "diagnostic shadowing" in women's health. It acts as a collaborative layer between patient narratives and clinical diagnosis.

---

## The Problem
Women face on average a **four-year diagnostic delay** compared to men across hundreds of conditions, according to a study of almost 7 million patients (Westergaard, D., Moseley, P., Sørup, F.K.H. et al. Population-wide analysis of differences in disease progression patterns in men and women. Nature Communications 10, 666 (2019)). This is often rooted in "diagnostic shadowing," where physical symptoms are wrongly attributed to mental health issues. This is rarely malice, rather, it is a byproduct of cognitive fatigue and a medical literature gap treating male physiology as the default.

## The Solution
LUCIA uses a **Dual-Stream Architecture** to separate the "listening" from the "auditing":
* **For the Clinician:** Synthesizes narratives into structured **Review of Systems (ROS)** data.
* **For the Patient:** Flags potential bias using the **AXIOM Knowledge Base** and generates neutral advocacy questions.

---
## **1\. Architecture & Workflow ("The Dual-Stream Engine")**

LUCIA utilizes a **Multi-Agent Orchestration** built on the Google Agent Development Kit (ADK). The system processes the patient's subjective narrative through four distinct stages to create a structured clinical asset.

### Why Agents? (Not just prompts)
1.  **Specialization:** A single LLM tends to hallucinate compliancy (agreeing with the doctor). We separate the **Scribe** (Agent 1) from the **Auditor** (Agent 2) to create an intentional adversarial check.
2.  **Statefulness:** The `InMemorySessionService` maintains the evolving context of the patient's story.
3.  **Verifiable Grounding:** The `bias_analyzer` uses a custom tool (`get_bias_implications`) to check findings against medical definitions, preventing hallucinated accusations.

### **The 4-Stage Pipeline**

![Workflow](./images/workflow.png "LUCIA workflow")

### The Pipeline
1.  **Parallel Layer:**
    * `symptom_mapper`: Extracts *only* patient-reported sensations (ignoring doctor labels).
    * `bias_analyzer`: Audits the interaction for specific bias markers using the AXIOM tool.
2.  **Sequential Layer:**
    * `advocacy_generator`: Converts findings into a Q&A script.
    * `report_formatter`: Compiles the final "Patient Advocacy & Consultation Aid."

---

## **2\. Project Structure**

```text
lucia_agent/
├── images/                   # Project assets (logos, diagrams)
├── lucia_deploy/             # Deployment artifacts for Vertex AI Agent Engine
│   ├── .agent_engine_config.json
│   ├── agent.py              # Deployment-specific agent logic
│   ├── requirements.txt
│   └── .env
├── main_agent/               # Core application logic
│   ├── __init__.py
│   └── agent.py              # Root Agent, Sub-agents, and Orchestration logic
├── tests/                    # Integration and Unit tests
│   ├── README.md
│   └── test_agent.py         # Main integration runner script
├── .env                      # Environment variables (Excluded from Git)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── LICENSE
```

---

## **3\. Installation & Setup**

### **Prerequisites**

* **Python 3.10+** (Required for Google ADK) 
* **Google Cloud Project** with **Gemini API** enabled. 
* **Google API Key**

### **Step 1: Clone and Environment**
```bash
git clone https://github.com/innacampo/lucia_agent.git
cd lucia_agent 

# Create a virtual environment 
python3 -m venv venv 

# Activate the virtual environment 
source venv/bin/activate 
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```
### **Step 3: Configuration**

Create a .env file in the root directory. **Do not commit this file.**
```bash
# .env file
GOOGLE_API_KEY="your_actual_api_key_here"
GOOGLE_GENAI_USE_VERTEXAI=0
```

---

## **4\. Usage & Testing**

We use a manual integration test script to verify the agent's behavior against specific patient narratives.

To run the integration test:
```bash
python -m tests.test_agent
```

---

## **5\. Demo Scenario: The "Perimenopause" Dismissal**

In this scenario, a 48-year-old user shares a frustrating interaction regarding autoimmune-like symptoms.

## Step 1: The Narrative (Input)  
*User:* "I've been waking up with stiff, swollen joints in my hands and feet for three months. The fatigue is so bad I have to nap in my car at lunch. I saw a new doctor today. I tried to show him the swelling, but he barely looked. He told me that at 48, this is just classic perimenopause and 'empty nest syndrome' making me depressed. He didn't order any blood work. He just told me to lose 10 pounds and try meditation to calm my 'nerves' because women get so anxious at this stage of life."

## Step 2: The Logic (Internal Monologue & Tool Usage)   
* **Agent 1 (Symptom Mapper):** Extracts Symptoms and assigns them to clusters:
    * stiff joints in my hands and feet $\\to$ pain cluster
    * fatigue $\\to$ fatigue cluster
    * swollen joints in my hands and feet $\\to$ musculoskeletal cluster

* **Agent 2 (Bias Analyzer):** Detects bias markers in the narrative (attribution of physical swelling to 'nerves') and queries the AXIOM Knowledge Base.
    * **Tool Call:** `get_bias_implications(bias_type="ageism_bias")`
        * **Output:** "Dismissing a patient's medical concerns as a normal or inevitable part of aging. This can prevent the timely diagnosis and treatment of serious conditions like heart disease, cancer, or neurological issues."
    * **Tool Call:** `get_bias_implications(bias_type="gender_bias")`
        * **Output:** "Often results in women's pain being taken less seriously or misdiagnosed, particularly in cardiovascular and autoimmune diseases."

* **Agent 3 (Advocacy generator):** Generates advocacy questions for the patient

## Step 3: The Output (Advocacy Report)  
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

---

## **6\. Cloud Deployment (Vertex AI Agent Engine)**

LUCIA is designed to run on Google Cloud's Vertex AI Agent Engine.
To deploy the contents of the `lucia_deploy` directory:
```bash
adk deploy agent_engine --project=$PROJECT_ID --region=$deployed_region lucia_deploy --agent_engine_config_file=lucia_deploy/.agent_engine_config.json
```

---

## **7\. Future Vision**

This capstone demonstrates LUCIA's immediate utility, but its long-term value lies in longitudinal observation.

* **For Researchers:** Future iterations will allow women to donate anonymized data to AXIOM, creating the "Big Data" needed to update guidelines.
* **For Clinicians:** Provides a "longitudinal view" of a patient's journey, revealing cyclical patterns invisible in snapshot appointments.

This project is licensed under the Apache 2.0 License.

*Submitted for the 5-Day AI Agents Intensive Course with Google Capstone Project*

![Bridge](./images/bridge.png "LUCIA bridge") 
