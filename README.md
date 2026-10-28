<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Build an AI Job Posting Analyzer

**Project Link:** [View Project](https://nextwork.ai/projects/72bf9516-9c3a-47c1-a1f4-3e187a623539)

**Author:** TAnimation TV  
**Email:** thandomzobe9@gmail.com

---

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/72bf9516-9c3a-47c1-a1f4-3e187a623539_2gi4kz7p)

## Project Overview: AI-Powered Job Market Analysis

### What this pipeline accomplishes

In this project, I'm building... using... so that I can learn and grow my skills

## Defining the Data Schema with Pydantic

### Setting up the project environment

In this step, I'm setting up my project environment and defining the data structure so that I can successfully extract specific details from unstructured job postings. By creating the JobPosting Pydantic schema, I'm providing the AI with a strict blueprint so it returns clean, structured JSON data instead of a messy block of text that my Python script would have to parse manually.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/72bf9516-9c3a-47c1-a1f4-3e187a623539_jbe5mtpc)

### Schema design decisions

My schema defines fields including job_title, company_name, required_skills, experience_level, salary_min, salary_max, and work_type.

The fields salary_min and salary_max are marked as Optional because job postings often do not include explicit salary information. By using Optional[int] in Pydantic, we tell the AI that it is perfectly valid to return null for these fields if no salary is mentioned. This prevents the AI from hallucinating a fake number or crashing the pipeline just because a salary wasn't listed in the text.

## Building the Gemini Extraction Pipeline

### Automating structured data extraction

In this step, I'm building the core extraction functions and processing loop so that I can automate the data extraction process. Specifically, I am setting up the API calls with Pydantic schemas to get clean JSON, and adding a loop with error handling and time.sleep() to safely process multiple job postings at once without crashing due to API rate limits.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/72bf9516-9c3a-47c1-a1f4-3e187a623539_alimxnu6)

### How structured output config works

The config passes the schema (specifically JobPosting.model_json_schema()) which tells Gemini to return the data in a strict JSON format matching that exact structure. This ensures the AI outputs specific fields like job_title, company_name, and salary_min instead of a plain text paragraph, making it easy to process in our code.

## Visualizing Job Market Insights

### Turning extracted data into charts

In this step, I'm building the data visualization function so that I can transform the raw extracted JSON data into actionable insights. Specifically, I am using Pandas to explode and count the skills, group salaries by experience level, and calculate work type distributions. Then, I am using Matplotlib to generate three clear charts (top_skills.png, salary_by_level.png, and work_type.png) so that a recruiter can instantly understand market trends without looking at the raw data.

![Image](https://nextwork.ai/vibrant_lavender_shy_sheep/uploads/72bf9516-9c3a-47c1-a1f4-3e187a623539_6j10mssa)

### Key insight from the skills analysis

Based on the top_skills.png chart, Python appears most frequently across the job postings. It is requested in 5 out of the 8 successfully extracted postings.

## AI Readiness Scoring: Multi-Pass LLM Analysis

### Top AI-focused role identified by Gemini

In this project extension, the highest scoring job was Entry-level Machine Learning Engineer at NeuralPath AI, which received a perfect [10/10] score. The AI identified this as a deeply AI-focused role because it explicitly requires a strong machine learning/technical stack (specifically mentioning PyTorch, scikit-learn, and transformers) and involves building AI-specific infrastructure.

This was closely followed by the Lead Data Scientist and Senior ML Ops Engineer, which both scored a [9/10] for requiring valuable applied ML experience and ML pipeline infrastructure (like MLflow), respectively.

## Reflections and Key Takeaways

### Tools and concepts mastered

Key Tools I used include: Python, Pandas, Matplotlib, Pydantic (for data validation and schemas), Google Gemini API (and later the NVIDIA NIM API via the OpenAI SDK to bypass rate limits), and JSON.

Key concepts I learnt include:

Multi-Pass LLM Pipelines: Chaining multiple AI calls where the first extracts data and the second analyzes it (scoring AI readiness), which is a production pattern for complex tasks.

Structured Outputs: Using Pydantic schemas to force the LLM to return strict JSON objects instead of unstructured text, ensuring the data is reliable and easy to parse into a DataFrame.

API Rate Limiting & Error Handling: Handling HTTP 429 (Too Many Requests) errors and daily quotas by adding time.sleep() delays, switching API providers (from Gemini to NVIDIA), and writing fallback logic to prevent the script from crashing.

Data Visualization: Transforming extracted JSON data into actionable insights using Pandas and Matplotlib (bar charts, pie charts, and horizontal bar charts).

### Time and challenges

This project took me approximately 2 to 3 hours to complete.

The most challenging part was dealing with the API rate limits and quota errors (specifically the HTTP 429 errors). Because I was using a free-tier API, I ran out of daily requests for the Gemini model. To fix this, I had to troubleshoot the errors, switch to a completely different provider (NVIDIA NIM), update the code to use the OpenAI Python SDK format, and handle the JSON structured output logic to ensure the Pydantic models still worked correctly.

I did this project today to learn how to... Another skill I want to learn is...

---

*Built with [NextWork](https://nextwork.ai) - [View this project](https://nextwork.ai/projects/72bf9516-9c3a-47c1-a1f4-3e187a623539)*
