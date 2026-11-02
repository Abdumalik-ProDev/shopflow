import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRegister } from "@/features/auth/hooks/useAuthForms";
import { registerSchema } from "@/features/auth/schemas/auth";
import type { RegisterFormData } from "@/features/auth/schemas/auth";
import { Link } from "react-router-dom";
import { User as UserIcon, AlertCircle } from "lucide-react";

export default function RegisterPage() {
  const { mutate: registerUser, isPending, error } = useRegister();
  const {
    register: reg,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      role: "customer",
    },
  });

  const onSubmit = (data: RegisterFormData) => {
    registerUser({
      email: data.email,
      username: data.username,
      password: data.password,
      full_name: data.full_name,
      role: data.role || "customer",
    });
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
            <UserIcon className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-display font-bold text-charcoal-900">Create your account</h1>
          <p className="text-sm text-charcoal-600">
            Join ShopFlow as a shopper or marketplace merchant
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
            <Label htmlFor="full_name">Full name</Label>
            <Input id="full_name" placeholder="Jane Doe" {...reg("full_name")} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="jane@example.com" {...reg("email")} />
            {errors.email && <p className="text-xs text-red-600">{errors.email.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input id="username" placeholder="janedoe" {...reg("username")} />
            {errors.username && <p className="text-xs text-red-600">{errors.username.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="role">Account type</Label>
            <select
              id="role"
              {...reg("role")}
              className="flex h-10 w-full rounded-md border border-charcoal-300 bg-white px-3 py-2 text-sm text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="customer">Customer (Shop & Order)</option>
              <option value="seller">Seller (Merchant Storefront)</option>
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password (min 8 characters)</Label>
            <Input id="password" type="password" placeholder="••••••••" {...reg("password")} />
            {errors.password && <p className="text-xs text-red-600">{errors.password.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm password</Label>
            <Input id="confirmPassword" type="password" placeholder="••••••••" {...reg("confirmPassword")} />
            {errors.confirmPassword && (
              <p className="text-xs text-red-600">{errors.confirmPassword.message}</p>
            )}
          </div>
          <Button type="submit" className="w-full" disabled={isPending}>
            {isPending ? "Creating account..." : "Create account"}
          </Button>
        </form>

        <p className="text-center text-sm text-charcoal-600">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-indigo-900 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
