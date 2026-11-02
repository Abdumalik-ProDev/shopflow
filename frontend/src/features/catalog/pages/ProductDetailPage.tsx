import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { catalogApi } from "../api/catalog";
import { Link, useParams } from "react-router-dom";
import { useCart } from "@/stores/cart";
import { ArrowLeft, ShoppingCart, Tag, Package, Scale } from "lucide-react";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [addedFeedback, setAddedFeedback] = React.useState(false);
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
  if (error || !product) {
    return (
      <div className="text-center py-20 space-y-4">
        <p className="text-red-600 font-medium">{error || "Product not found."}</p>
        <Button variant="outline" asChild>
          <Link to="/catalog">Back to catalog</Link>
        </Button>
      </div>
    );
  }

  const handleAddToCart = () => {
    addItem({
      productId: product.id,
      name: product.name,
      price: product.price,
    });
    setAddedFeedback(true);
    setTimeout(() => setAddedFeedback(false), 1500);
  };

  return (
    <div className="flex flex-col lg:flex-row gap-8">
      <div className="lg:w-1/2">
        <div className="aspect-square bg-white border border-charcoal-200 rounded-2xl flex items-center justify-center shadow-sm">
          <Tag className="w-24 h-24 text-charcoal-400" />
        </div>
      </div>
      <div className="lg:w-1/2 flex flex-col gap-6">
        <div className="flex items-center justify-between gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link to="/catalog" className="flex items-center gap-1.5">
              <ArrowLeft className="w-4 h-4" /> Back to catalog
            </Link>
          </Button>
          <Badge variant="outline" className="text-base px-3 py-1 font-bold text-charcoal-900">
            ${product.price.toFixed(2)}
          </Badge>
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">{product.name}</CardTitle>
            <p className="text-xs text-charcoal-500 font-mono">SKU: {product.sku}</p>
          </CardHeader>
          <CardContent className="space-y-4 text-charcoal-600 text-sm leading-relaxed">
            <p>{product.description || "Authentic marketplace item from verified sellers."}</p>
            <div className="grid grid-cols-2 gap-3 pt-3 border-t border-charcoal-100 text-xs">
              <div className="flex items-center gap-2">
                <Package className="w-4 h-4 text-indigo-600" />
                <span>
                  Dimensions:{" "}
                  {product.length_cm
                    ? `${product.length_cm}×${product.width_cm}×${product.height_cm} cm`
                    : "Standard"}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Scale className="w-4 h-4 text-indigo-600" />
                <span>Weight: {product.weight_g ? `${product.weight_g} g` : "Standard"}</span>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex items-center justify-between gap-4 border-t border-charcoal-100 pt-4">
            <span className="text-sm font-medium text-charcoal-700 shrink-0">
              In Stock: <strong>{product.stock_quantity}</strong> units
            </span>
            <Button
              onClick={handleAddToCart}
              disabled={!product.is_active || product.stock_quantity === 0}
              className="w-full max-w-xs"
            >
              <ShoppingCart className="w-4 h-4 mr-2" />
              {addedFeedback ? "Added to cart!" : "Add to cart"}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
