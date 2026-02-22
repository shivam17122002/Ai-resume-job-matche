import type { JobCreateRequest, JobResponse } from "../types/job";
import apiClient from "../api/client";


export const createJob = async (
  job: JobCreateRequest
): Promise<JobResponse> => {
  const response = await apiClient.post<JobResponse>("/jobs", job);
  return response.data;
};

export const searchJobs = async (params: {
  q?: string;
  location?: string;
  skills?: string[];
  page?: number;
  size?: number;
}) => {
  const response = await apiClient.get("/search/jobs", { params });
  return response.data;
};
