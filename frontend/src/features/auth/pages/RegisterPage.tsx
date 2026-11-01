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
import { User as UserIcon, Mail, Lock } from "lucide-react";

export default function RegisterPage() {
  const { mutate: register, isPending } = useRegister();
  const {
    register: reg,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({ resolver: zodResolver(registerSchema) });

  const onSubmit = (data: RegisterFormData) => {
    const { confirmPassword, ...payload } = data;
    register({
      email: data.email,
      username: data.username,
      password: data.password,
      full_name: data.full_name,
      role: data.role || "customer",
    });
  };

  return (
    <div className="space-y-6">
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
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" {...reg("password")} />
          {errors.password && <p className="text-xs text-red-600">{errors.password.message}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm password</Label>
          <Input id="confirmPassword" type="password" {...reg("confirmPassword")} />
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
        <Link to="/auth/login" className="font-medium text-indigo-900 hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
