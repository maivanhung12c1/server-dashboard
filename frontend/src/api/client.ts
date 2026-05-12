import axios from "axios";

const client = axios.create({
  baseURL: "/api/v1",
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
});

const HTTP_ERRORS: Record<number, string> = {
  400: "Invalid request. Please check your input.",
  401: "Unauthorized. Please log in.",
  403: "You don't have permission to perform this action.",
  404: "The requested resource was not found.",
  409: "Conflict — this resource already exists.",
  422: "Validation failed. Please check your input.",
  429: "Too many requests. Please slow down.",
  500: "Server error. Please try again later.",
  502: "Service unavailable. Please try again later.",
  503: "Service unavailable. Please try again later.",
};

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const status: number | undefined = error.response?.status;
    const message =
      error.response?.data?.msg ||
      error.response?.data?.detail ||
      (status ? HTTP_ERRORS[status] : undefined) ||
      (error.code === "ECONNABORTED" ? "Request timed out. Please try again." : undefined) ||
      (!error.response ? "Cannot connect to server. Please check your connection." : undefined) ||
      "An unexpected error occurred";
    return Promise.reject(new Error(message));
  },
);

export default client;
