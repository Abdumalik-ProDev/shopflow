export interface ProductResponse {
  id: string;
  sku: string;
  name: string;
  description?: string | null;
  price: number;
  stock_quantity: number;
  category_id?: string | null;
  seller_id?: string | null;
  is_active: boolean;
  weight_g?: number | null;
  length_cm?: number | null;
  height_cm?: number | null;
  width_cm?: number | null;
  photos_qty?: number | null;
}

export interface CategoryResponse {
  id: string;
  name: string;
  name_english?: string | null;
}

export interface CategoryCreateRequest {
  name: string;
  name_english?: string;
}

export interface ProductCreateRequest {
  sku: string;
  name: string;
  description?: string;
  price: number;
  stock_quantity?: number;
  category_id?: string;
  seller_id?: string;
  is_active?: boolean;
  weight_g?: number;
  length_cm?: number;
  height_cm?: number;
  width_cm?: number;
  photos_qty?: number;
}

export interface ProductUpdateRequest {
  name?: string;
  description?: string;
  price?: number;
  stock_quantity?: number;
  category_id?: string;
  seller_id?: string;
  is_active?: boolean;
}

export type { ProductResponse as Product };
