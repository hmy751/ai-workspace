export const baseURL = "https://dummyjson.com";
export class APIError extends Error {
    status;
    code;
    data;
    reset;
    constructor(message, status, code, data, reset) {
        super(message);
        this.status = status;
        this.code = code;
        this.data = data;
        this.reset = reset;
        this.name = "APIError";
    }
}
const createAbortController = (timeout) => {
    const controller = new AbortController();
    setTimeout(() => controller.abort(), timeout);
    return controller;
};
const handleResponse = async (response) => {
    const contentType = response.headers.get("content-type");
    const isJSON = contentType?.includes("application/json");
    const data = isJSON ? await response.json() : await response.text();
    if (!response.ok) {
        throw new APIError(data.message || response.statusText, response.status, data.code || "UNKNOWN_ERROR", data);
    }
    return data;
};
const handleError = (error) => {
    if (error instanceof APIError)
        throw error;
    if (error instanceof Error) {
        if (error.name === "AbortError") {
            throw new APIError("요청 시간이 초과되었습니다", 408, "REQUEST_TIMEOUT");
        }
        throw new APIError("네트워크 에러가 발생했습니다", 0, "NETWORK_ERROR", error);
    }
    throw new APIError("알 수 없는 에러가 발생했습니다", 0, "UNKNOWN_ERROR", error);
};
const createHttpClient = (defaultConfig) => {
    const request = async (url, options = {}) => {
        try {
            const finalOptions = { ...options };
            const controller = createAbortController(finalOptions.timeout || defaultConfig.timeout);
            const fullURL = `${defaultConfig.baseURL}/${url}`;
            const response = await fetch(fullURL, {
                ...finalOptions,
                headers: {
                    ...defaultConfig.headers,
                    ...finalOptions.headers,
                },
                signal: controller.signal,
            });
            return handleResponse(response);
        }
        catch (error) {
            throw handleError(error);
        }
    };
    return {
        get: (url, options) => request(url, { ...options, method: "GET" }),
        post: (url, data, options) => request(url, {
            ...options,
            method: "POST",
            body: JSON.stringify(data),
        }),
        put: (url, data, options) => request(url, {
            ...options,
            method: "PUT",
            body: JSON.stringify(data),
        }),
        delete: (url, options) => request(url, { ...options, method: "DELETE" }),
    };
};
const fetcher = createHttpClient({
    baseURL: baseURL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});
export default fetcher;
//# sourceMappingURL=fetcher.js.map