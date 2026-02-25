import { useState } from "react";
import { isAxiosError } from "axios";
import { login, register } from "../services/authService";

type ErrorDetail = { msg?: string };

const getApiErrorMessage = (err: unknown, fallback: string): string => {
  if (!isAxiosError(err)) return fallback;

  const detail = err.response?.data?.detail as string | ErrorDetail[] | undefined;
  if (typeof detail === "string" && detail.trim()) return detail;
  if (Array.isArray(detail) && detail.length > 0) return detail[0]?.msg || fallback;

  return fallback;
};

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const doLogin = async () => {
    try {
      await login({ email, password });
      setMessage("Logged in");
    } catch (err: unknown) {
      setMessage(getApiErrorMessage(err, "Login failed"));
    }
  };

  const doRegister = async () => {
    try {
      await register({ email, password });
      setMessage("Registered, you can now login");
    } catch (err: unknown) {
      setMessage(getApiErrorMessage(err, "Registration failed"));
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg border border-slate-200 p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900">Welcome Back</h2>
        <p className="text-sm text-slate-500 mt-1">Login or create a new account</p>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
          <input className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" placeholder="your@email.com" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
          <input className="w-full border-2 border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100 transition-colors" placeholder="••••••••" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
      </div>
      
      <div className="mt-6 flex gap-3">
        <button onClick={doLogin} className="flex-1 px-4 py-2 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700 transition-colors shadow-md">Login</button>
        <button onClick={doRegister} className="flex-1 px-4 py-2 rounded-lg border-2 border-slate-300 text-slate-700 font-medium hover:bg-slate-50 transition-colors">Register</button>
      </div>
      
      {message && <div className={`mt-4 p-3 rounded-lg text-sm font-medium ${message.includes('Logged') || message.includes('Registered') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>{message}</div>}
    </div>
  );
};

export default Login;
