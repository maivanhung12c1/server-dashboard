// Server
export interface Server {
  id: string;
  ip_address: string;
  country: string;
  name: string;
  os: string;
  os_version: string;
  platform: string;
  arch: string;
  status: "Online" | "Offline";
  created_at: string; // DD/MM/YYYY HH:mm:ss
  updated_at: string;
}

export interface CreateServerPayload {
  ip_address: string;
  country: string;
  name: string;
  os: string;
  os_version: string;
  platform: string;
  arch: string;
  status?: "Online" | "Offline";
}

export interface UpdateServerPayload {
  ip_address?: string;
  country?: string;
  name?: string;
  os?: string;
  os_version?: string;
  platform?: string;
  arch?: string;
  status?: "Online" | "Offline";
}

// Pagination
export interface PageData<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}

// API Response Envelope
export interface ApiResponse<T = unknown> {
  code: number;
  msg: string;
  data: T;
}

// Activity
export interface Activity {
  id: string;
  server_id: string;
  server_name: string;
  action: "created" | "updated" | "deleted" | "renamed";
  detail: string;
  timestamp: string;
}

// Statistics
export interface NameCount {
  name: string;
  count: number;
}

export interface OverviewStats {
  total_servers: number;
  by_os: NameCount[];
  by_platform: NameCount[];
  by_arch: NameCount[];
  by_status: NameCount[];
}

export interface TimeseriesPoint {
  date: string;
  count: number;
}

export interface TimeseriesStats {
  range: "24h" | "7d" | "30d" | "custom";
  start: string;
  end: string;
  total_servers: number;
  new_in_range: number;
  timeseries: TimeseriesPoint[];
}

// Map
export interface MapServer {
  id: string;
  name: string;
  ip_address: string;
  status: string;
}

export interface MapCountryData {
  country: string;
  count: number;
  servers: MapServer[];
}

// Filters
export interface ServerFilters {
  name?: string;
  status?: string;
  country?: string;
  os?: string;
  platform?: string;
  page?: number;
  size?: number;
}
