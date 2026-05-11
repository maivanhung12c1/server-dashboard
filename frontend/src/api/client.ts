import axios from "axios";

const client = axios.create({
  baseURL: "/api/v1",
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    // Extract message from our standard {code, msg, data} envelope
    const message =
      error.response?.data?.msg ||
      error.response?.data?.detail ||
      error.message ||
      "An unexpected error occurred";
    return Promise.reject(new Error(message));
  },
);

export default client;
