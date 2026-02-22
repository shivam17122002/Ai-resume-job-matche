import apiClient from "../api/client";
import type { UserCreate } from "../types/auth";

export const register = async (payload: UserCreate) => {
  const res = await apiClient.post("/auth/register", payload);
  return res.data;
};

export const login = async (payload: UserCreate) => {
  const res = await apiClient.post("/auth/login", payload);
  // persist token
  if (res.data?.access_token) {
    localStorage.setItem("access_token", res.data.access_token);
  }
  return res.data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
};
