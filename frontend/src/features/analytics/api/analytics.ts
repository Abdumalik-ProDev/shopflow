import { api } from "@/app/config/api";

export interface AnalyticsKPI {
  label: string;
  value: number;
  delta?: number;
  delta_percent?: number;
}

export interface SalesPoint {
  date: string;
  sales: number;
  orders: number;
}

export interface AnalyticsSummary {
  kpis: AnalyticsKPI[];
  sales_over_time: SalesPoint[];
}

export const analyticsApi = {
  async getSummary(): Promise<AnalyticsSummary> {
    const res = await api.get<AnalyticsSummary>("/analytics/summary");
    return res.data;
  },
};

export interface Recommendation {
  product_id: string;
  product_name?: string;
  price?: number;
  category_name?: string;
  score: number;
  reason: string;
}

export interface RecommendationsResponse {
  customer_id: string;
  recommendations: Recommendation[];
}

export const recommendationsApi = {
  async getForCustomer(customerId: string, limit = 10): Promise<RecommendationsResponse> {
    const res = await api.get<RecommendationsResponse>(`/recommendations/customer/${customerId}`, {
      params: { limit },
    });
    return res.data;
  },
};
