import { useState } from "react";
import ResumeUpload from "./pages/ResumeUpload";
import JobCreate from "./pages/JobCreate";
import JobSearch from "./pages/JobSearch";
import Login from "./pages/Login";
import NavBar from "./components/NavBar";

function App() {
  const [page, setPage] = useState<"home" | "upload" | "jobs" | "search" | "login">("home");

  return (
    <div className="min-h-screen bg-gradient-to-b from-sky-50 via-white to-slate-50 text-slate-800">
      <NavBar onNavigate={setPage} />

      <main className="container mx-auto px-4 py-8">
        {page === "home" && (
          <section className="rounded-xl p-8 bg-white shadow-lg">
            <h1 className="text-3xl font-extrabold text-sky-700">AI Resume Analyzer</h1>
            <p className="mt-2 text-slate-600">Upload a resume, extract skills using AI, and match to jobs instantly.</p>
            <div className="mt-6 flex gap-4">
              <button onClick={() => setPage("upload")} className="px-4 py-2 rounded bg-sky-600 text-white hover:opacity-90">Upload Resume</button>
              <button onClick={() => setPage("jobs")} className="px-4 py-2 rounded border border-sky-200 text-sky-700">Create Job</button>
            </div>
          </section>
        )}

        {page === "upload" && (
          <section>
            <ResumeUpload />
          </section>
        )}

        {page === "jobs" && (
          <section>
            <JobCreate />
          </section>
        )}

        {page === "search" && (
          <section>
            <JobSearch />
          </section>
        )}
        {page === "login" && (
          <section>
            <Login />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
