import { useState } from "react";
import { isAxiosError } from "axios";
import { uploadResume, analyzeResume } from "../services/resumeService";

const ResumeUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string>("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a resume PDF");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const uploadResponse = await uploadResume(file);
      setResumeId(uploadResponse.id);

      const analysisResponse = await analyzeResume(uploadResponse.id);

      setMessage(
        `Skills: ${analysisResponse.skills?.join(", ") || "(none)"}`
      );
    } catch (error: unknown) {
      console.error(error);
      if (isAxiosError<{ detail?: string }>(error)) {
        setMessage(error.response?.data?.detail || "Error uploading or analyzing resume");
      } else {
        setMessage("Error uploading or analyzing resume");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-slate-900">Upload Resume</h2>
          <p className="text-sm text-slate-500 mt-2">PDF only, up to 10MB. We extract skills and experience using AI.</p>
        </div>

        <div className="mt-6">
          <label className="block">
            <span className="text-sm font-medium text-slate-700 mb-2 block">Select PDF File</span>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-sky-100 file:text-sky-700 file:font-medium hover:file:bg-sky-200 transition-colors cursor-pointer border-2 border-dashed border-slate-300 rounded-lg p-4"
            />
          </label>
        </div>

        <div className="mt-6 flex items-center gap-4">
          <button onClick={handleUpload} disabled={loading} className="px-6 py-2 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors flex items-center gap-2">
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/></svg>
                <span>Processing...</span>
              </>
            ) : (
              "Upload & Analyze"
            )}
          </button>

          {resumeId && <div className="text-sm text-slate-600">Resume ID: <span className="font-bold text-sky-700 bg-sky-50 px-3 py-1 rounded-lg">{resumeId}</span></div>}
        </div>

        {message && (
          <div className="mt-6 p-4 rounded-lg bg-sky-50 border border-sky-200 text-sky-800 font-medium">{message}</div>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;
