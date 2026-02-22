import React from "react";
import type { JobResponse } from "../types/job";

type Props = {
  job: JobResponse;
  onView?: (id: number) => void;
};

const JobCard: React.FC<Props> = ({ job, onView }) => {
  return (
    <div className="bg-white rounded-lg shadow-md border border-slate-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start gap-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-slate-900">{job.title}</h3>
          <div className="text-sm text-slate-600 mt-1 font-medium">{job.company}</div>
          <div className="text-sm text-slate-500 mt-1">{job.location || 'Location not specified'}</div>
        </div>
        <div className="text-right">
          <div className="text-sm px-3 py-1 rounded-lg bg-sky-50 text-sky-700 font-bold whitespace-nowrap">{job.salary || "—"}</div>
        </div>
      </div>

      <p className="mt-4 text-sm text-slate-600 line-clamp-2">{job.description}</p>

      {(job.required_skills || []).length > 0 && (
        <div className="mt-4">
          <div className="text-xs font-semibold text-slate-700 mb-2">Required Skills:</div>
          <div className="flex flex-wrap gap-2">
            {(job.required_skills || []).map((s) => (
              <span key={s} className="text-xs bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full font-medium">{s}</span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 flex justify-end">
        <button onClick={() => onView?.(job.id)} className="text-sm px-4 py-2 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700 transition-colors">
          View Details
        </button>
      </div>
    </div>
  );
};

export default JobCard;
