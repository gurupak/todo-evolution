export interface ErrorDetail {
  field: string;
  message: string;
  code?: string;
}

export interface ErrorResponse {
  detail: string;
  errors?: ErrorDetail[];
}

export interface DeleteResponse {
  message: string;
  id: string;
}
