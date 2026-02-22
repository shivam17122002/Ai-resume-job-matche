import type { MatchResult } from "../types/match";
import apiClient from "../api/client";

export const matchResumeToJob = async (
  resumeId: number,
  jobId: number
): Promise<MatchResult> => {
  const response = await apiClient.get<MatchResult>(
    `/match/resume/${resumeId}/job/${jobId}`
  );
  return response.data;
};

export const topResumesForJob = async (jobId: number, limit = 5) => {
  const response = await apiClient.get(
    `/match/job/${jobId}/top-resumes`,
    { params: { limit } }
  );
  return response.data;
};
