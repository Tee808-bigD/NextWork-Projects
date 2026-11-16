from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class JobPosting(BaseModel):
    """Schema for structured job posting extraction."""

    job_title: str = Field(description="The job title or role name.")
    company_name: str = Field(description="The name of the hiring company.")
    required_skills: List[str] = Field(
        description="List of required technical skills and tools mentioned."
    )
    experience_level: Literal["entry", "mid", "senior", "lead"] = Field(
        description="The seniority level: entry, mid, senior, or lead."
    )
    salary_min: Optional[int] = Field(
        description="Minimum salary in USD, or null if not mentioned."
    )
    salary_max: Optional[int] = Field(
        description="Maximum salary in USD, or null if not mentioned."
    )
    work_type: Literal["remote", "hybrid", "onsite"] = Field(
        description="The work arrangement: remote, hybrid, or onsite."
    )


class AIReadinessScore(BaseModel):
    """Schema for evaluating how well a candidate matches a job posting."""
    
    overall_score: int = Field(
        description="An overall readiness score from 0 to 100."
    )
    matching_skills: List[str] = Field(
        description="List of skills the candidate has that match the job."
    )
    missing_skills: List[str] = Field(
        description="List of required skills the candidate is missing."
    )
    recommendation: str = Field(
        description="A brief summary of what the candidate should focus on to improve their score."
    )
