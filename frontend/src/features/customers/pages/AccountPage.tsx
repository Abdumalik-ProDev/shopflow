import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/app/providers/AuthProvider";
import { User as UserIcon, Mail, ShieldCheck } from "lucide-react";
import { customersApi } from "@/features/customers/api/customers";

export default function AccountPage() {
  const { user, isAuthenticated } = useAuth();
  const [customer, setCustomer] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    if (user?.id) {
      customersApi.get(user.id).then(setCustomer).finally(() => setIsPending(false));
    } else {
      setIsPending(false);
    }
  }, [user]);

  if (!isAuthenticated) return null;
  if (isPending) return <div className="animate-pulse h-64 rounded-xl bg-charcoal-200" />;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-display font-bold text-charcoal-900">My account</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-charcoal-200 flex items-center justify-center text-charcoal-600">
                <UserIcon className="w-6 h-6" />
              </div>
              <div>
                <p className="font-semibold">{user?.full_name || user?.username}</p>
                <p className="text-sm text-charcoal-500">{user?.email}</p>
              </div>
            </div>
            {customer && (
              <div className="space-y-2 text-sm">
                <p><strong>City:</strong> {customer.customer_city}</p>
                <p><strong>State:</strong> {customer.customer_state}</p>
                <p><strong>ZIP:</strong> {customer.customer_zip_code_prefix}</p>
              </div>
            )}
            <div className="flex items-center gap-3">
              <Badge variant={user.role === "admin" ? "destructive" : "secondary"}>
                {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
              </Badge>
              {user.is_active ? <Badge variant="default">Active</Badge> : <Badge variant="destructive">Inactive</Badge>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Security</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <span>Password protection enabled</span>
            </div>
            <Button variant="outline" className="w-full">
              Change password
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
