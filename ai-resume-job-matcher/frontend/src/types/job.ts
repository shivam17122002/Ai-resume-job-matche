export interface JobCreateRequest {
  title: string;
  company: string;
  description: string;
  required_skills: string[];
  location: string;
  salary: string;
}

export interface JobResponse {
  id: number;
  title: string;
  company: string;
  description: string;
  required_skills: string[];
  location: string;
  salary: string;
}
