import { api } from "@/app/config/api";

export interface OrderItemCreate {
  product_id: string;
  seller_id: string;
  price: number;
  freight_value?: number;
  quantity?: number;
}

export interface OrderCreate {
  customer_id: string;
  items: OrderItemCreate[];
  estimated_delivery_date?: string;
}

export interface OrderItemResponse {
  id: string;
  order_id: string;
  product_id: string;
  seller_id: string;
  price: number;
  freight_value: number;
  quantity: number;
}

export interface OrderResponse {
  id: string;
  customer_id: string;
  status: string;
  purchase_timestamp?: string;
  total: number;
  items: OrderItemResponse[];
}

export interface OrderStatusUpdate {
  status: string;
}

export const ordersApi = {
  async list(params?: {
    skip?: number;
    limit?: number;
    customer_id?: string;
    status?: string;
  }): Promise<OrderResponse[]> {
    const res = await api.get<OrderResponse[]>("/orders", { params });
    return res.data;
  },
  async get(id: string): Promise<OrderResponse> {
    const res = await api.get<OrderResponse>(`/orders/${id}`);
    return res.data;
  },
  async create(payload: OrderCreate): Promise<OrderResponse> {
    const res = await api.post<OrderResponse>("/orders", payload);
    return res.data;
  },
  async updateStatus(id: string, status: string): Promise<OrderResponse> {
    const res = await api.patch<OrderResponse>(`/orders/${id}/status`, { status });
    return res.data;
  },
};

export const paymentsApi = {
  async create(payload: {
    order_id: string;
    payment_type?: string;
    payment_installments?: number;
    payment_value: number;
  }): Promise<any> {
    const res = await api.post("/payments", payload);
    return res.data;
  },
  async listByOrder(orderId: string): Promise<any[]> {
    const res = await api.get(`/payments/order/${orderId}`);
    return res.data;
  },
};

export const reviewsApi = {
  async create(payload: {
    order_id: string;
    review_score: number;
    comment_title?: string;
    comment_message?: string;
  }): Promise<any> {
    const res = await api.post("/reviews", payload);
    return res.data;
  },
  async listByOrder(orderId: string): Promise<any[]> {
    const res = await api.get(`/reviews/order/${orderId}`);
    return res.data;
  },
};
