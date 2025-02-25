import { RequestOptions, ApiResponse } from '../types/api';

const BASE_URL = import.meta.env.VITE_IP_BACKEND_MAIN;

const DEFAULT_HEADERS: HeadersInit = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8',
};

/**
 * Obtiene el token de autenticación del localStorage
 */
const getAuthToken = (): string | null => {
    try {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user).token.access_token : null;
    } catch {
        return null;
    }
};

/**
 * Construye las cabeceras de la petición
 */
const buildHeaders = (requireAuth: boolean = false): HeadersInit => {
    const headers = { ...DEFAULT_HEADERS };
    
    if (requireAuth) {
        const token = getAuthToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    
    return headers;
};

/**
 * Procesa la respuesta de la API
 */
const processResponse = async <T>(response: Response): Promise<ApiResponse<T>> => {
    const data = await response.json() as T;
    
    return {
        error: response.status !== 200 ? new Error(`${response.status}: ${response.statusText}`) : null,
        value: data
    };
};

/**
 * Construye los parámetros de la petición
 */
const buildRequestOptions = (
    method: string,
    params: any = {},
    requireAuth: boolean = false
): RequestInit => {
    const options: RequestInit = {
        method,
        headers: buildHeaders(requireAuth)
    };

    if (method !== 'GET' && Object.keys(params).length > 0) {
        options.body = JSON.stringify(params);
    }

    return options;
};

/**
 * Realiza una petición HTTP
 */
async function fetchApi<T>(
    url: string,
    params: any = {},
    method: string = 'GET',
    requireAuth: boolean = false
): Promise<ApiResponse<T>> {
    const options = buildRequestOptions(method, params, requireAuth);
    const fullUrl = method === 'GET' && Object.keys(params).length > 0
        ? `${BASE_URL}${url}?${new URLSearchParams(params)}`
        : `${BASE_URL}${url}`;

    console.log("fullUrl", fullUrl);

    try {
        const response = await fetch(fullUrl, options);
        return await processResponse<T>(response);
    } catch (error) {
        return {
            error: error instanceof Error ? error : new Error('Unknown error'),
            value: null
        };
    }
}

// Métodos HTTP exportados
export const http = {
    get: <T>(url: string, params = {}, requireAuth = false) => 
        fetchApi<T>(url, params, 'GET', requireAuth),
    
    post: <T>(url: string, params = {}, requireAuth = false) => 
        fetchApi<T>(url, params, 'POST', requireAuth),
    
    put: <T>(url: string, params = {}, requireAuth = false) => 
        fetchApi<T>(url, params, 'PUT', requireAuth),
    
    delete: <T>(url: string, params = {}, requireAuth = false) => 
        fetchApi<T>(url, params, 'DELETE', requireAuth)
};
