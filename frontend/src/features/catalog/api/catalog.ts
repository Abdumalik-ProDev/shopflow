import { api } from "@/app/config/api";
import type { ProductResponse, CategoryCreateRequest, CategoryResponse } from "@/types/catalog";

export const catalogApi = {
  async listProducts(params?: {
    skip?: number;
    limit?: number;
    category_id?: string;
    seller_id?: string;
    is_active?: boolean;
  }): Promise<ProductResponse[]> {
    const res = await api.get<ProductResponse[]>("/products", { params });
    return res.data;
  },
  async getProduct(id: string): Promise<ProductResponse> {
    const res = await api.get<ProductResponse>(`/products/${id}`);
    return res.data;
  },
  async createProduct(payload: Partial<ProductResponse>): Promise<ProductResponse> {
    const res = await api.post<ProductResponse>("/products", payload);
    return res.data;
  },
  async updateProduct(id: string, payload: Partial<ProductResponse>): Promise<ProductResponse> {
    const res = await api.patch<ProductResponse>(`/products/${id}`, payload);
    return res.data;
  },
  async adjustStock(id: string, delta: number): Promise<ProductResponse> {
    const res = await api.post<ProductResponse>(`/products/${id}/stock`, { delta });
    return res.data;
  },
  async listCategories(params?: { skip?: number; limit?: number }): Promise<CategoryResponse[]> {
    const res = await api.get<CategoryResponse[]>("/products/categories", { params });
    return res.data;
  },
  async createCategory(payload: CategoryCreateRequest): Promise<CategoryResponse> {
    const res = await api.post<CategoryResponse>("/products/categories", payload);
    return res.data;
  },
};
