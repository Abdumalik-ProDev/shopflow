import { useAuth } from "@/app/providers/AuthProvider";
import { useMutation } from "@tanstack/react-query";
import { login, register } from "@/features/auth/api";
import { loginSchema, registerSchema } from "@/features/auth/schemas/auth";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

export function useLogin() {
  const { login: setToken } = useAuth();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: login,
    onSuccess: (data: any) => {
      setToken(data.access_token);
      navigate("/");
    },
  });
}

export function useRegister() {
  const navigate = useNavigate();
  return useMutation({
    mutationFn: register,
    onSuccess: () => {
      navigate("/auth/login");
    },
  });
}

export { loginSchema, registerSchema };
