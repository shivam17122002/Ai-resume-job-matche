import React, { useState } from "react";
import { searchJobs } from "../services/jobService";
import JobCard from "../components/JobCard";
import type { JobResponse } from "../types/job";

type SearchHit = {
  job_id: number | string;
  source: {
    title: string;
    company: string;
    description: string;
    required_skills?: string[];
    location?: string;
    salary?: string;
  };
};

type SearchJobsResponse = {
  results?: SearchHit[];
};

const JobSearch: React.FC = () => {
  const [q, setQ] = useState("");
  const [location, setLocation] = useState("");
  const [skills, setSkills] = useState("");
  const [results, setResults] = useState<JobResponse[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const resp = await searchJobs({ q, location, skills: skills ? skills.split(",").map(s => s.trim()) : undefined }) as SearchJobsResponse;
      setResults(resp.results?.map((r) => ({
        id: Number(r.job_id),
        title: r.source.title,
        company: r.source.company,
        description: r.source.description,
        required_skills: r.source.required_skills || [],
        location: r.source.location || "",
        salary: r.source.salary || "",
      })) || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-slate-900">Find Jobs</h2>
          <p className="text-sm text-slate-500 mt-2">Search jobs by keyword, location, and skills.</p>
        </div>

        <div className="mt-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Keywords</label>
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="e.g. React, Frontend, Python" className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Location</label>
              <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="e.g. New York, Remote" className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Skills</label>
              <input value={skills} onChange={(e) => setSkills(e.target.value)} placeholder="e.g. TypeScript, Node.js" className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
            </div>
          </div>
        </div>

        <div className="mt-6 flex gap-3">
          <button onClick={handleSearch} className="px-6 py-2 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700 transition-colors flex items-center gap-2 shadow-md">
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/></svg>
                <span>Searching...</span>
              </>
            ) : (
              <span>Search Jobs</span>
            )}
          </button>
          {results.length > 0 && <div className="px-4 py-2 bg-slate-100 rounded-lg text-sm font-medium text-slate-700">Found {results.length} job{results.length !== 1 ? 's' : ''}</div>}
        </div>
      </div>

      {results.length > 0 && (
        <div className="mt-8">
          <h3 className="text-2xl font-bold text-slate-900 mb-4">Search Results</h3>
          <div className="grid grid-cols-1 gap-4">
            {results.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
        </div>
      )}
      {results.length === 0 && q && (
        <div className="mt-8 p-8 text-center bg-slate-50 rounded-lg">
          <p className="text-slate-600">No jobs found. Try adjusting your search criteria.</p>
        </div>
      )}
    </div>
  );
};

export default JobSearch;
