import { api } from "@/app/config/api";

export interface CustomerResponse {
  id: string;
  customer_unique_id: string;
  customer_zip_code_prefix: string;
  customer_city: string;
  customer_state: string;
  user_id?: string;
}

export interface CustomerCreateRequest {
  customer_unique_id: string;
  customer_zip_code_prefix: string;
  customer_city: string;
  customer_state: string;
}

export interface CustomerUpdateRequest {
  customer_zip_code_prefix?: string;
  customer_city?: string;
  customer_state?: string;
}

export const customersApi = {
  async list(params?: { skip?: number; limit?: number }): Promise<CustomerResponse[]> {
    const res = await api.get<CustomerResponse[]>("/customers", { params });
    return res.data;
  },
  async get(id: string): Promise<CustomerResponse> {
    const res = await api.get<CustomerResponse>(`/customers/${id}`);
    return res.data;
  },
  async create(payload: CustomerCreateRequest): Promise<CustomerResponse> {
    const res = await api.post<CustomerResponse>("/customers", payload);
    return res.data;
  },
  async update(id: string, payload: CustomerUpdateRequest): Promise<CustomerResponse> {
    const res = await api.patch<CustomerResponse>(`/customers/${id}`, payload);
    return res.data;
  },
};

export interface SellerResponse {
  id: string;
  seller_zip_code_prefix: string;
  seller_city: string;
  seller_state: string;
  user_id?: string;
}

export interface SellerCreateRequest {
  seller_zip_code_prefix: string;
  seller_city: string;
  seller_state: string;
}

export const sellersApi = {
  async list(params?: { skip?: number; limit?: number }): Promise<SellerResponse[]> {
    const res = await api.get<SellerResponse[]>("/sellers", { params });
    return res.data;
  },
  async get(id: string): Promise<SellerResponse> {
    const res = await api.get<SellerResponse>(`/sellers/${id}`);
    return res.data;
  },
  async create(payload: SellerCreateRequest): Promise<SellerResponse> {
    const res = await api.post<SellerResponse>("/sellers", payload);
    return res.data;
  },
};
