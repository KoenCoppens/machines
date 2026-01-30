const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!res.ok) {
    const message = await res.text();
    throw new Error(message || "Request failed");
  }
  return res.json() as Promise<T>;
}

export interface Account {
  id: string;
  account_number: string;
  name: string;
  phone?: string;
  email?: string;
  billing_city?: string;
  billing_country?: string;
  language?: string;
}

export interface Contact {
  id: string;
  display_name?: string;
  email?: string;
  role?: string;
}

export interface Location {
  id: string;
  name?: string;
  location_code: string;
  city?: string;
}

export interface Machine {
  id: string;
  machine_name: string;
  machine_number?: string;
  warranty_end_date?: string;
  status?: string;
}

export interface Alert {
  id: string;
  alert_type: string;
  alert_date: string;
  due_date?: string;
  status: string;
  assigned_to?: string;
}

export const api = {
  getAccounts: (search?: string) =>
    request<Account[]>(`/accounts/?${search ? `search=${encodeURIComponent(search)}` : ""}`),
  getAccount: (id: string) => request<Account>(`/accounts/${id}`),
  getContacts: (accountId: string) => request<Contact[]>(`/contacts/?account_id=${accountId}`),
  getLocations: (accountId: string) => request<Location[]>(`/locations/?account_id=${accountId}`),
  getMachines: (accountId: string) => request<Machine[]>(`/machines/?account_id=${accountId}`),
  getAlerts: (status?: string) => request<Alert[]>(`/alerts/?${status ? `status=${status}` : ""}`),
  updateAlert: (id: string, payload: Partial<Alert>) =>
    request<Alert>(`/alerts/${id}`, { method: "PATCH", body: JSON.stringify(payload) })
};
