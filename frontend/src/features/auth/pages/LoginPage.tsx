import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLogin } from "@/features/auth/hooks/useAuthForms";
import { loginSchema } from "@/features/auth/schemas/auth";
import type { LoginFormData } from "@/features/auth/schemas/auth";
import { Link } from "react-router-dom";
import { Lock, AlertCircle, Sparkles } from "lucide-react";

export default function LoginPage() {
  const { mutate: login, isPending, error } = useLogin();
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<LoginFormData>({ resolver: zodResolver(loginSchema) });

  const onSubmit = (data: LoginFormData) => {
    login({ username: data.username, password: data.password });
  };

  const quickLogin = (identifier: string) => {
    setValue("username", identifier);
    setValue("password", "Password123!");
    login({ username: identifier, password: "Password123!" });
  };

  const apiErrorMsg =
    (error as any)?.response?.data?.detail ||
    (error as Error)?.message ||
    null;

  return (
    <div className="max-w-md mx-auto py-8">
      <div className="bg-white rounded-2xl border border-charcoal-200 shadow-sm p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-indigo-900 text-amber-400 flex items-center justify-center mx-auto font-bold">
            <Lock className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-display font-bold text-charcoal-900">Welcome back</h1>
          <p className="text-sm text-charcoal-600">
            Sign in with your username or email address
          </p>
        </div>

        {apiErrorMsg && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{String(apiErrorMsg)}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">Username or Email</Label>
            <Input
              id="username"
              placeholder="admin@shopflow.com or admin"
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

        <div className="pt-4 border-t border-charcoal-100 space-y-3">
          <div className="flex items-center justify-center gap-1.5 text-xs font-medium text-charcoal-500">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>1-Click Demo Accounts</span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="text-xs"
              disabled={isPending}
              onClick={() => quickLogin("customer@shopflow.com")}
            >
              Customer
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="text-xs"
              disabled={isPending}
              onClick={() => quickLogin("seller@shopflow.com")}
            >
              Seller
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="text-xs"
              disabled={isPending}
              onClick={() => quickLogin("admin@shopflow.com")}
            >
              Admin
            </Button>
          </div>
        </div>

        <p className="text-center text-sm text-charcoal-600">
          Don't have an account?{" "}
          <Link to="/register" className="font-semibold text-indigo-900 hover:underline">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
