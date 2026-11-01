import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { catalogApi } from "../api/catalog";
import { useCart } from "@/stores/cart";
import { Link } from "react-router-dom";
import { ArrowRight, ShoppingCart, Tag } from "lucide-react";

export default function CatalogPage() {
  const [products, setProducts] = React.useState<any[]>([]);

  const [isPending, setIsPending] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const { addItem } = useCart();

  React.useEffect(() => {
    catalogApi
      .listProducts({ limit: 50 })
      .then((data: any[]) => {
        setProducts(data);
        setIsPending(false);
      })
      .catch(() => {
        setError("Failed to load products.");
        setIsPending(false);
      });
  }, []);

  if (isPending) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }
  if (error) return <div className="text-red-600 text-center py-20">{error}</div>;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-display font-bold text-charcoal-900">Catalog</h1>
        <Button variant="outline" asChild>
          <Link to="/" className="flex items-center gap-2">
            <ArrowRight className="w-4 h-4" /> Browse all
          </Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <Card key={product.id} className="group hover:shadow-md transition">
            <div className="aspect-square bg-charcoal-100 rounded-lg mb-4 flex items-center justify-center">
              <Tag className="w-12 h-12 text-charcoal-400" />
            </div>
            <CardHeader>
              <CardTitle className="text-lg">{product.name}</CardTitle>
              <Badge variant="outline">${product.price.toFixed(2)}</Badge>
            </CardHeader>
            <CardContent className="text-charcoal-600 text-sm line-clamp-2">
              {product.description || "No description available."}
            </CardContent>
            <CardFooter className="flex items-center justify-between gap-2">
              <span className="text-sm font-medium text-charcoal-900">
                Stock: {product.stock_quantity}
              </span>
              <Button
                size="sm"
                onClick={() =>
                  addItem({
                    productId: product.id,
                    name: product.name,
                    price: product.price,
                  })
                }
                disabled={!product.is_active || product.stock_quantity === 0}
              >
                <ShoppingCart className="w-4 h-4" /> Add
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}

function SkeletonCard() {
  return (
    <Card className="p-0">
      <div className="aspect-square bg-charcoal-200 rounded-lg mb-4" />
      <div className="px-4 py-2">
        <div className="h-4 bg-charcoal-200 rounded w-3/4 mb-2" />
        <div className="h-4 bg-charcoal-200 rounded w-1/2" />
      </div>
    </Card>
  );
}
