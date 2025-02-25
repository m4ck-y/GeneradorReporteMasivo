export interface RequestOptions {
    method: string;
    headers: HeadersInit;
    body?: BodyInit;
}

export interface ApiResponse<T> {
    error: Error | null;
    value: T | null;
} 