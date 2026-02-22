import type {ResumeUploadResponse,ResumeAnalysisResponse,} from "../types/resume";
import apiClient from "../api/client";


export const uploadResume = async (
  file: File
): Promise<ResumeUploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<ResumeUploadResponse>(
    "/resumes/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const analyzeResume = async (
  resumeId: number
): Promise<ResumeAnalysisResponse> => {
  const response = await apiClient.post<ResumeAnalysisResponse>(
    `/resumes/${resumeId}/analyze`
  );
  return response.data;
};
