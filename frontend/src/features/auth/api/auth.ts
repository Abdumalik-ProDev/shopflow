import { api } from "@/app/config/api";

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  role?: string;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  role: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user?: User;
}

export async function login(data: LoginRequest): Promise<TokenResponse> {
  const res = await api.post<TokenResponse>("/auth/login", data);
  return res.data;
}

export async function register(data: RegisterRequest): Promise<User> {
  const res = await api.post<User>("/auth/register", data);
  return res.data;
}

export async function me(): Promise<User> {
  const res = await api.get<User>("/auth/me");
  return res.data;
}

export async function changePassword(data: {
  current_password: string;
  new_password: string;
}): Promise<{ message: string }> {
  const res = await api.post<{ message: string }>("/auth/change-password", data);
  return res.data;
}
