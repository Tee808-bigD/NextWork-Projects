import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
from models import JobPosting, AIReadinessScore

# Set up the NVIDIA client (uses the OpenAI SDK format)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

# Active NVIDIA model 
ACTIVE_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"

def load_job_postings(csv_path: str) -> pd.DataFrame:
    """Load job postings from CSV file."""
    return pd.read_csv(csv_path)
    
def extract_job_data(description: str) -> JobPosting:
    """Extract structured data from a single job posting using NVIDIA NIM."""
    prompt = f"""Extract the structured job posting information from the following text.
If salary information is not explicitly mentioned, set salary_min and salary_max to null.

Job Posting:
{description}"""

    response = client.chat.completions.create(
        model=ACTIVE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=1024,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "JobPosting",
                "schema": JobPosting.model_json_schema()
            }
        }
    )
    
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from model")
        
    return JobPosting.model_validate_json(content)
    
def score_ai_readiness(description: str) -> AIReadinessScore:
    """Score a job posting's AI readiness using NVIDIA NIM."""
    prompt = f"""Analyze the following job posting and rate how AI/ML focused the role is.
Score from 1 (not AI related at all) to 10 (deeply AI/ML focused).
Consider mentions of AI tools, ML frameworks, data science techniques, and AI-adjacent responsibilities.

Job Posting:
{description}"""

    response = client.chat.completions.create(
        model=ACTIVE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=1024,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "AIReadinessScore",
                "schema": AIReadinessScore.model_json_schema()
            }
        }
    )
    
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from model")
        
    return AIReadinessScore.model_validate_json(content)
    
    
def process_all_postings(df: pd.DataFrame) -> list[dict]:
    """Process all job postings through the extraction pipeline."""
    results = []
    total = len(df)

    for index, row in df.iterrows():
        print(f"Processing posting {index + 1}/{total}...")
        try:
            job_data = extract_job_data(row["description"])
            results.append(job_data.model_dump())
        except Exception as e:
            print(f"  Error processing posting {row['id']}: {e}")
            continue
        time.sleep(2)

    return results

def process_ai_readiness(df: pd.DataFrame) -> list[dict]:
    """Score all job postings for AI readiness."""
    scores = []
    total = len(df)

    for index, row in df.iterrows():
        print(f"Scoring posting {index + 1}/{total}...")
        try:
            ai_score = score_ai_readiness(row["description"])
            scores.append(ai_score.model_dump())
        except Exception as e:
            print(f"  Error scoring posting {row['id']}: {e}")
            continue
        time.sleep(2)

    return scores
 
def create_visualizations(results_df: pd.DataFrame) -> None:
    """Create and save matplotlib visualizations."""
    # 1. Top skills bar chart
    all_skills = results_df["required_skills"].explode()
    skill_counts = all_skills.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    skill_counts.plot(kind="barh", ax=ax, color="steelblue")
    ax.set_xlabel("Number of Postings")
    ax.set_title("Top 10 Most Requested Skills")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_skills.png", dpi=150)
    plt.close()
    print("Saved: top_skills.png")

    # 2. Salary by experience level
    salary_data = results_df.dropna(subset=["salary_min", "salary_max"])
    if not salary_data.empty:
        salary_avg = salary_data.groupby("experience_level")[
            ["salary_min", "salary_max"]
        ].mean()

        fig, ax = plt.subplots(figsize=(8, 5))
        salary_avg.plot(kind="bar", ax=ax, color=["#2196F3", "#4CAF50"])
        ax.set_ylabel("Salary (USD)")
        ax.set_title("Average Salary Range by Experience Level")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.legend(["Min Salary", "Max Salary"])
        plt.tight_layout()
        plt.savefig("salary_by_level.png", dpi=150)
        plt.close()
        print("Saved: salary_by_level.png")

    # 3. Work type distribution
    work_counts = results_df["work_type"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    work_counts.plot(
        kind="pie", ax=ax, autopct="%1.1f%%", colors=["#66BB6A", "#42A5F5", "#FFA726"]
    )
    ax.set_ylabel("")
    ax.set_title("Work Type Distribution")
    plt.tight_layout()
    plt.savefig("work_type.png", dpi=150)
    plt.close()
    print("Saved: work_type.png")

def create_ai_readiness_chart(results_df: pd.DataFrame) -> None:
    """Create AI readiness score visualization."""
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(results_df["job_title"], results_df["ai_readiness_score"], color="darkorange")
    ax.set_xlabel("AI Readiness Score (1-10)")
    ax.set_title("AI Readiness Score by Job Posting")
    ax.set_xlim(0, 10)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("ai_readiness.png", dpi=150)
    plt.close()
    print("Saved: ai_readiness.png")
    
def main():
    """Main pipeline execution."""
    api_key = os.environ.get("NVIDIA_API_KEY")
    
    if not api_key:
        print("Error: NVIDIA_API_KEY environment variable not set.")
        return 

    print("Loading job postings...")
    postings_df = load_job_postings("job_postings.csv")
    print(f"Found {len(postings_df)} postings.\n")

    print("Starting AI extraction pipeline...")
    print("-" * 40)
    results = process_all_postings(postings_df)
    print("-" * 40)
    print(f"\nSuccessfully extracted {len(results)}/{len(postings_df)} postings.\n")

    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        print("No data extracted. Exiting pipeline.")
        return

    print("Extracted Data:")
    print(results_df[["job_title", "company_name", "experience_level", "work_type"]].to_string())
    
    print("\nGenerating visualizations...")
    create_visualizations(results_df)
    
    # Secret Mission: AI Readiness Scoring
    print("\n" + "=" * 40)
    print("SECRET MISSION: AI Readiness Scoring")
    print("=" * 40)
    
    ai_scores = process_ai_readiness(postings_df)

    if len(ai_scores) > 0:
        scored_df = results_df.iloc[:len(ai_scores)].copy()
        
        # FIXED: Mapped the correct keys from models.py
        scored_df["ai_readiness_score"] = [s["overall_score"] for s in ai_scores]
        scored_df["ai_reasoning"] = [s["recommendation"] for s in ai_scores]
        
        # Combined the two skill lists into one text string for the DataFrame
        scored_df["ai_skills_mentioned"] = [
            f"Matches: {', '.join(s['matching_skills'])} | Missing: {', '.join(s['missing_skills'])}"
            for s in ai_scores
        ]

        ranked = scored_df.sort_values("ai_readiness_score", ascending=False)
        print("\nTop AI Jobs Recommendation:")
        print("-" * 40)
        for _, row in ranked.iterrows():
            print(f"  [{row['ai_readiness_score']}/10] {row['job_title']} at {row['company_name']}")
            print(f"         {row['ai_reasoning']}")
            print()

        create_ai_readiness_chart(scored_df)
        print("\nSecret Mission complete!")
    else:
        print("\n[Warning] Scoring phase failed completely.")

if __name__ == "__main__":
    main()
