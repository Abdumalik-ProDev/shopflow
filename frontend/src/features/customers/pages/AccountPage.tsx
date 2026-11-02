import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/app/providers/AuthProvider";
import { User as UserIcon, ShieldCheck, CheckCircle2, AlertCircle } from "lucide-react";
import { customersApi } from "@/features/customers/api/customers";
import { changePassword } from "@/features/auth/api/auth";
import { Link } from "react-router-dom";

export default function AccountPage() {
  const { user, isAuthenticated } = useAuth();
  const [customer, setCustomer] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);

  // Location update state
  const [city, setCity] = React.useState("");
  const [stateCode, setStateCode] = React.useState("");
  const [zip, setZip] = React.useState("");
  const [profileStatus, setProfileStatus] = React.useState<string | null>(null);

  // Password change state
  const [showPwForm, setShowPwForm] = React.useState(false);
  const [currentPassword, setCurrentPassword] = React.useState("");
  const [newPassword, setNewPassword] = React.useState("");
  const [pwStatus, setPwStatus] = React.useState<{ ok: boolean; msg: string } | null>(null);

  React.useEffect(() => {
    if (user?.id) {
      customersApi
        .get(user.id)
        .then((c) => {
          setCustomer(c);
          setCity(c.customer_city || "");
          setStateCode(c.customer_state || "");
          setZip(c.customer_zip_code_prefix || "");
        })
        .catch(() => {})
        .finally(() => setIsPending(false));
    } else {
      setIsPending(false);
    }
  }, [user]);

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto text-center py-20 bg-white rounded-2xl p-8 border border-charcoal-200 shadow-sm">
        <UserIcon className="w-12 h-12 text-charcoal-400 mx-auto mb-3" />
        <h2 className="text-xl font-bold text-charcoal-900">Sign in required</h2>
        <p className="mt-1 text-sm text-charcoal-600 mb-6">
          Please sign in to view and manage your account profile.
        </p>
        <Button asChild>
          <Link to="/login">Sign in</Link>
        </Button>
      </div>
    );
  }

  if (isPending || !user) {
    return <div className="animate-pulse h-64 rounded-xl bg-charcoal-200" />;
  }

  const handleSaveLocation = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileStatus(null);
    try {
      const targetId = customer?.id || user.id;
      const updated = await customersApi.update(targetId, {
        customer_city: city,
        customer_state: stateCode,
        customer_zip_code_prefix: zip,
      });
      setCustomer(updated);
      setProfileStatus("Location details saved!");
    } catch {
      setProfileStatus("Could not update location details.");
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwStatus(null);
    if (newPassword.length < 8) {
      setPwStatus({ ok: false, msg: "New password must be at least 8 characters." });
      return;
    }
    try {
      const res = await changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setPwStatus({ ok: true, msg: res.message });
      setCurrentPassword("");
      setNewPassword("");
      setShowPwForm(false);
    } catch (err: any) {
      setPwStatus({
        ok: false,
        msg: err?.response?.data?.detail || "Failed to update password.",
      });
    }
  };

  const roleLabel = user.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : "Customer";

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-display font-bold text-charcoal-900">My Account</h1>
        <div className="flex items-center gap-2">
          {user.role === "seller" && (
            <Button variant="outline" size="sm" asChild>
              <Link to="/seller">Seller Dashboard</Link>
            </Button>
          )}
          {user.role === "admin" && (
            <Button variant="outline" size="sm" asChild>
              <Link to="/admin">Admin Analytics</Link>
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Profile & Shipping Address</CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-900 font-bold">
                <UserIcon className="w-6 h-6" />
              </div>
              <div>
                <p className="font-semibold text-charcoal-900">{user.full_name || user.username}</p>
                <p className="text-sm text-charcoal-500">{user.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Badge variant={user.role === "admin" ? "destructive" : "secondary"}>
                {roleLabel}
              </Badge>
              {user.is_active ? (
                <Badge variant="default">Active</Badge>
              ) : (
                <Badge variant="destructive">Inactive</Badge>
              )}
            </div>

            {customer && (
              <form onSubmit={handleSaveLocation} className="space-y-3 pt-3 border-t border-charcoal-100">
                <div className="grid grid-cols-3 gap-3">
                  <div className="col-span-2 space-y-1">
                    <Label htmlFor="acct_city">City</Label>
                    <Input id="acct_city" value={city} onChange={(e) => setCity(e.target.value)} />
                  </div>
                  <div className="col-span-1 space-y-1">
                    <Label htmlFor="acct_state">State</Label>
                    <Input id="acct_state" maxLength={2} value={stateCode} onChange={(e) => setStateCode(e.target.value)} />
                  </div>
                </div>
                <div className="space-y-1">
                  <Label htmlFor="acct_zip">ZIP Prefix</Label>
                  <Input id="acct_zip" value={zip} onChange={(e) => setZip(e.target.value)} />
                </div>
                {profileStatus && (
                  <p className="text-xs text-emerald-600 font-medium">{profileStatus}</p>
                )}
                <Button type="submit" size="sm" variant="outline">
                  Save address
                </Button>
              </form>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Security & Credentials</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <span className="text-sm text-charcoal-700">Bcrypt password & JWT token protection active</span>
            </div>

            {pwStatus && (
              <div
                className={`p-3 rounded-lg text-xs flex items-center gap-2 ${
                  pwStatus.ok
                    ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                    : "bg-red-50 text-red-700 border border-red-200"
                }`}
              >
                {pwStatus.ok ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                <span>{pwStatus.msg}</span>
              </div>
            )}

            {!showPwForm ? (
              <Button variant="outline" className="w-full" onClick={() => setShowPwForm(true)}>
                Change password
              </Button>
            ) : (
              <form onSubmit={handleChangePassword} className="space-y-3 pt-2 border-t border-charcoal-100">
                <div className="space-y-1">
                  <Label htmlFor="curr_pw">Current password</Label>
                  <Input
                    id="curr_pw"
                    type="password"
                    required
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="new_pw">New password (min 8 chars)</Label>
                  <Input
                    id="new_pw"
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    Update password
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant="outline"
                    onClick={() => setShowPwForm(false)}
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
