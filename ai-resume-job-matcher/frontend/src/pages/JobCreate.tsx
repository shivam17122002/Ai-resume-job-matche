import { useState } from "react";
import { createJob } from "../services/jobService";

const JobCreate = () => {
  const [form, setForm] = useState({
    title: "",
    company: "",
    description: "",
    required_skills: "",
    location: "",
    salary: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await createJob({
        title: form.title,
        company: form.company,
        description: form.description,
        required_skills: form.required_skills.split(",").map(s => s.trim()),
        location: form.location,
        salary: form.salary,
      });

      setMessage("✅ Job created successfully");
      setForm({ title: "", company: "", description: "", required_skills: "", location: "", salary: "" });
    } catch (err: any) {
      console.error(err);
      setMessage(err?.response?.data?.detail || "❌ Failed to create job");
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-slate-900">Create Job Posting</h2>
          <p className="text-sm text-slate-500 mt-2">Add a job posting to index and make it searchable.</p>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Job Title *</label>
            <input name="title" value={form.title} placeholder="e.g. Senior React Developer" onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Company *</label>
            <input name="company" value={form.company} placeholder="e.g. Acme Inc" onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Job Description *</label>
            <textarea name="description" value={form.description} placeholder="Describe the role and responsibilities..." onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 h-32 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors resize-none" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Required Skills *</label>
            <input name="required_skills" value={form.required_skills} placeholder="React, TypeScript, Node.js" onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Location</label>
              <input name="location" value={form.location} placeholder="e.g. San Francisco, CA" onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Salary</label>
              <input name="salary" value={form.salary} placeholder="e.g. $120k - $150k" onChange={handleChange} className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" />
            </div>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button onClick={handleSubmit} className="px-6 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-colors shadow-md hover:shadow-lg">
            Create Job
          </button>
          {message && <div className={`text-sm font-medium px-4 py-2 rounded-lg ${message.includes('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>{message}</div>}
        </div>
      </div>
    </div>
  );
};

export default JobCreate;
