import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLogin } from "@/features/auth/hooks/useAuthForms";
import { loginSchema } from "@/features/auth/schemas/auth";
import type { LoginFormData } from "@/features/auth/schemas/auth";
import { Link, useNavigate } from "react-router-dom";
import { Lock, User as UserIcon } from "lucide-react";

export default function LoginPage() {
  const navigate = useNavigate();
  const { mutate: login, isPending } = useLogin();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({ resolver: zodResolver(loginSchema) });

  const onSubmit = (data: LoginFormData) => {
    login({ username: data.username, password: data.password });
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            placeholder="jane.doe"
            {...register("username")}
            className={errors.username ? "border-red-500" : ""}
          />
          {errors.username && <p className="text-xs text-red-600">{errors.username.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            {...register("password")}
            className={errors.password ? "border-red-500" : ""}
          />
          {errors.password && <p className="text-xs text-red-600">{errors.password.message}</p>}
        </div>
        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? "Signing in..." : "Sign in"}
        </Button>
      </form>
      <p className="text-center text-sm text-charcoal-600">
        Don't have an account?{" "}
        <Link to="/auth/register" className="font-medium text-indigo-900 hover:underline">
          Create one
        </Link>
      </p>
    </div>
  );
}
