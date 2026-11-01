import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { catalogApi } from "../api/catalog";
import { useParams } from "react-router-dom";
import { useCart } from "@/stores/cart";
import { ArrowLeft, ShoppingCart, Tag } from "lucide-react";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const { addItem } = useCart();

  React.useEffect(() => {
    if (!id) return;
    catalogApi
      .getProduct(id)
      .then((data: any) => {
        setProduct(data);
        setIsPending(false);
      })
      .catch(() => {
        setError("Product not found.");
        setIsPending(false);
      });
  }, [id]);

  if (isPending) return <div className="animate-pulse h-96 rounded-xl bg-charcoal-200" />;
  if (error || !product) return <div className="text-red-600 text-center py-20">{error}</div>;

  return (
    <div className="flex flex-col lg:flex-row gap-8">
      <div className="lg:w-1/2">
        <div className="aspect-square bg-charcoal-200 rounded-xl flex items-center justify-center">
          <Tag className="w-24 h-24 text-charcoal-400" />
        </div>
      </div>
      <div className="lg:w-1/2 flex flex-col gap-6">
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" asChild>
            <ArrowLeft className="w-4 h-4" /> Back to catalog
          </Button>
          <Badge variant="outline">${product.price.toFixed(2)}</Badge>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>{product.name}</CardTitle>
          </CardHeader>
          <CardContent className="text-charcoal-600 text-sm leading-relaxed">
            {product.description || "No description available."}
          </CardContent>
          <CardFooter>
            <div className="flex items-center justify-between">
              <span className="text-sm">Stock: {product.stock_quantity}</span>
              <Button
                onClick={() =>
                  addItem({
                    productId: product.id,
                    name: product.name,
                    price: product.price,
                  })
                }
                disabled={!product.is_active || product.stock_quantity === 0}
                className="w-full"
              >
                <ShoppingCart className="w-4 h-4 mr-2" /> Add to cart
              </Button>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
