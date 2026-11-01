import { useQuery } from "@tanstack/react-query";
import { catalogApi } from "../api/catalog";

export function useProducts() {
  return useQuery({
    queryKey: ["products"],
    queryFn: () => catalogApi.listProducts(),
  });
}

export function useProduct(id: string) {
  return useQuery({
    queryKey: ["product", id],
    queryFn: () => catalogApi.getProduct(id),
    enabled: !!id,
  });
}
