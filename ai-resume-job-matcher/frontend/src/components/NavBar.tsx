import React from "react";

type Props = {
  onNavigate: (page: "home" | "upload" | "jobs" | "search" | "login") => void;
};

const NavBar: React.FC<Props> = ({ onNavigate }) => {
  return (
    <header className="w-full bg-white shadow-md sticky top-0 z-40 border-b border-slate-200">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="text-xl font-bold text-sky-600">Resume Matcher</div>
        </div>

        <nav className="flex items-center gap-1">
          <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors" onClick={() => onNavigate("home")}>Home</button>
          <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors" onClick={() => onNavigate("upload")}>Upload</button>
          <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors" onClick={() => onNavigate("jobs")}>Create</button>
          <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors" onClick={() => onNavigate("search")}>Search</button>
          <button className="px-4 py-2 text-sm font-medium text-white bg-sky-600 hover:bg-sky-700 rounded-lg transition-colors" onClick={() => onNavigate("login")}>Login</button>
        </nav>
      </div>
    </header>
  );
};

export default NavBar;
