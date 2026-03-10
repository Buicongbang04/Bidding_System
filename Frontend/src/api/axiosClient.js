import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 60000
});

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const detail = error?.response?.data?.detail;
    if (detail) {
      if (typeof detail === "string") {
        return Promise.reject(new Error(detail));
      }

      if (typeof detail === "object") {
        return Promise.reject(
          new Error(detail.error_message || JSON.stringify(detail))
        );
      }
    }

    return Promise.reject(error);
  }
);

export default axiosClient;