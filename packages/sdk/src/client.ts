import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import type { paths } from './types';

export class GroundedCounsellingClient {
  private client: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:8000', config?: AxiosRequestConfig) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      ...config,
    });
  }

  setAuthToken(token: string) {
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  removeAuthToken() {
    delete this.client.defaults.headers.common['Authorization'];
  }

  // Health check
  async health() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.client.post('/api/v1/auth/login', {
      email,
      password,
    });
    return response.data;
  }

  async register(userData: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    role?: string;
  }) {
    const response = await this.client.post('/api/v1/auth/register', userData);
    return response.data;
  }

  async refreshToken(refreshToken: string) {
    const response = await this.client.post('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  }

  async logout() {
    const response = await this.client.post('/api/v1/auth/logout');
    return response.data;
  }

  // User endpoints
  async getCurrentUser() {
    const response = await this.client.get('/api/v1/users/me');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/api/v1/users/me', data);
    return response.data;
  }

  // Specialists endpoints
  async getSpecialists(params?: {
    skip?: number;
    limit?: number;
    specialization?: string;
  }) {
    const response = await this.client.get('/api/v1/specialists', { params });
    return response.data;
  }

  async getSpecialist(id: string) {
    const response = await this.client.get(`/api/v1/specialists/${id}`);
    return response.data;
  }

  // Booking endpoints
  async createBooking(data: {
    specialist_id: string;
    start_time: string;
    duration_minutes: number;
    notes?: string;
  }) {
    const response = await this.client.post('/api/v1/bookings', data);
    return response.data;
  }

  async getBookings(params?: {
    skip?: number;
    limit?: number;
    status?: string;
  }) {
    const response = await this.client.get('/api/v1/bookings', { params });
    return response.data;
  }

  async getBooking(id: string) {
    const response = await this.client.get(`/api/v1/bookings/${id}`);
    return response.data;
  }

  async updateBooking(id: string, data: any) {
    const response = await this.client.put(`/api/v1/bookings/${id}`, data);
    return response.data;
  }

  async cancelBooking(id: string) {
    const response = await this.client.delete(`/api/v1/bookings/${id}`);
    return response.data;
  }

  // Generic request method for custom endpoints
  async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.client.request(config);
    return response.data;
  }
}

export default GroundedCounsellingClient;