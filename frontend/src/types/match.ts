export interface MatchResult {
  match_score: number;
  verdict: string;
  matched_skills: string[];
  missing_skills: string[];
  experience_analysis: {
    resume_years: number;
    job_required_years: number | null;
    experience_score: number;
  };
  explanation: string;
}
