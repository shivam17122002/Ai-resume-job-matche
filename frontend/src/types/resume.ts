export interface ResumeUploadResponse {
  id: number;
  filename: string;
  message: string;
}

export interface ResumeAnalysisResponse {
  resume_id: number;
  role: string;
  skills: string[];
  experience_years: number;
}
