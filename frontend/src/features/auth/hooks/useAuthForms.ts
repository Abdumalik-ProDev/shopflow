import { useAuth } from "@/app/providers/AuthProvider";
import { useMutation } from "@tanstack/react-query";
import { login, register } from "@/features/auth/api";
import { loginSchema, registerSchema } from "@/features/auth/schemas/auth";
import { useNavigate } from "react-router-dom";

export function useLogin() {
  const { login: setAuth } = useAuth();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      setAuth(data.access_token, data.user);
      navigate("/");
    },
  });
}

export function useRegister() {
  const { login: setAuth } = useAuth();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: async (payload: Parameters<typeof register>[0]) => {
      await register(payload);
      return await login({ username: payload.username, password: payload.password });
    },
    onSuccess: (data) => {
      setAuth(data.access_token, data.user);
      navigate("/");
    },
  });
}

export { loginSchema, registerSchema };
