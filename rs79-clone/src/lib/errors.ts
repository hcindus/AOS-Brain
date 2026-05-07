/**
 * Custom Error Classes for RS-79 POS System
 * Provides structured error handling with HTTP status codes and error codes
 */

export class AppError extends Error {
  public readonly statusCode: number
  public readonly code: string
  public readonly isOperational: boolean

  constructor(
    message: string,
    statusCode: number = 500,
    code: string = 'INTERNAL_ERROR',
    isOperational: boolean = true
  ) {
    super(message)
    this.statusCode = statusCode
    this.code = code
    this.isOperational = isOperational

    // Maintain proper stack trace for error location
    Error.captureStackTrace(this, this.constructor)

    // Set the prototype explicitly for instanceof checks
    Object.setPrototypeOf(this, AppError.prototype)
  }

  /**
   * Serialize error to JSON format for API responses
   */
  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
      },
    }
  }
}

/**
 * Authentication Error - Invalid credentials, unauthorized access
 */
export class AuthError extends AppError {
  constructor(message: string = 'Authentication failed') {
    super(message, 401, 'AUTH_ERROR')
    Object.setPrototypeOf(this, AuthError.prototype)
  }
}

/**
 * Authorization Error - Insufficient permissions
 */
export class ForbiddenError extends AppError {
  constructor(message: string = 'Access denied') {
    super(message, 403, 'FORBIDDEN')
    Object.setPrototypeOf(this, ForbiddenError.prototype)
  }
}

/**
 * Validation Error - Invalid input data
 */
export class ValidationError extends AppError {
  public readonly fieldErrors?: Record<string, string[]>

  constructor(
    message: string = 'Validation failed',
    fieldErrors?: Record<string, string[]>
  ) {
    super(message, 400, 'VALIDATION_ERROR')
    this.fieldErrors = fieldErrors
    Object.setPrototypeOf(this, ValidationError.prototype)
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        fieldErrors: this.fieldErrors,
      },
    }
  }
}

/**
 * Payment Error - Payment processing issues
 */
export class PaymentError extends AppError {
  public readonly paymentCode?: string

  constructor(message: string = 'Payment failed', paymentCode?: string) {
    super(message, 402, 'PAYMENT_ERROR')
    this.paymentCode = paymentCode
    Object.setPrototypeOf(this, PaymentError.prototype)
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        paymentCode: this.paymentCode,
      },
    }
  }
}

/**
 * Not Found Error - Resource not found
 */
export class NotFoundError extends AppError {
  public readonly resource?: string
  public readonly resourceId?: string

  constructor(
    message: string = 'Resource not found',
    resource?: string,
    resourceId?: string
  ) {
    super(message, 404, 'NOT_FOUND')
    this.resource = resource
    this.resourceId = resourceId
    Object.setPrototypeOf(this, NotFoundError.prototype)
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        resource: this.resource,
        resourceId: this.resourceId,
      },
    }
  }
}

/**
 * Conflict Error - Resource already exists or conflict
 */
export class ConflictError extends AppError {
  constructor(message: string = 'Resource conflict') {
    super(message, 409, 'CONFLICT')
    Object.setPrototypeOf(this, ConflictError.prototype)
  }
}

/**
 * Rate Limit Error - Too many requests
 */
export class RateLimitError extends AppError {
  public readonly retryAfter?: number

  constructor(message: string = 'Rate limit exceeded', retryAfter?: number) {
    super(message, 429, 'RATE_LIMIT')
    this.retryAfter = retryAfter
    Object.setPrototypeOf(this, RateLimitError.prototype)
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        retryAfter: this.retryAfter,
      },
    }
  }
}

/**
 * Database Error - Database connection or query issues
 */
export class DatabaseError extends AppError {
  constructor(message: string = 'Database error') {
    super(message, 500, 'DATABASE_ERROR', false)
    Object.setPrototypeOf(this, DatabaseError.prototype)
  }
}

/**
 * External Service Error - Third-party service failures
 */
export class ExternalServiceError extends AppError {
  public readonly service?: string

  constructor(message: string = 'External service error', service?: string) {
    super(message, 502, 'EXTERNAL_SERVICE_ERROR', false)
    this.service = service
    Object.setPrototypeOf(this, ExternalServiceError.prototype)
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        service: this.service,
      },
    }
  }
}

/**
 * Session Error - Session management issues
 */
export class SessionError extends AppError {
  constructor(message: string = 'Session error') {
    super(message, 440, 'SESSION_ERROR')
    Object.setPrototypeOf(this, SessionError.prototype)
  }
}

/**
 * Error codes enum for consistent error handling
 */
export enum ErrorCode {
  // Auth errors (401)
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  TOKEN_INVALID = 'TOKEN_INVALID',
  UNAUTHORIZED = 'UNAUTHORIZED',

  // Forbidden errors (403)
  INSUFFICIENT_PERMISSIONS = 'INSUFFICIENT_PERMISSIONS',
  ROLE_REQUIRED = 'ROLE_REQUIRED',

  // Validation errors (400)
  INVALID_INPUT = 'INVALID_INPUT',
  MISSING_REQUIRED_FIELD = 'MISSING_REQUIRED_FIELD',
  INVALID_FORMAT = 'INVALID_FORMAT',
  INVALID_ENUM_VALUE = 'INVALID_ENUM_VALUE',

  // Payment errors (402)
  PAYMENT_DECLINED = 'PAYMENT_DECLINED',
  INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS',
  INVALID_PAYMENT_METHOD = 'INVALID_PAYMENT_METHOD',
  GIFT_CARD_INACTIVE = 'GIFT_CARD_INACTIVE',
  GIFT_CARD_EXPIRED = 'GIFT_CARD_EXPIRED',
  GIFT_CARD_INSUFFICIENT = 'GIFT_CARD_INSUFFICIENT',
  STORE_CREDIT_INSUFFICIENT = 'STORE_CREDIT_INSUFFICIENT',

  // Not found errors (404)
  ORDER_NOT_FOUND = 'ORDER_NOT_FOUND',
  CUSTOMER_NOT_FOUND = 'CUSTOMER_NOT_FOUND',
  ITEM_NOT_FOUND = 'ITEM_NOT_FOUND',
  GIFT_CARD_NOT_FOUND = 'GIFT_CARD_NOT_FOUND',
  CLERK_NOT_FOUND = 'CLERK_NOT_FOUND',
  PAYMENT_NOT_FOUND = 'PAYMENT_NOT_FOUND',

  // Conflict errors (409)
  DUPLICATE_ENTRY = 'DUPLICATE_ENTRY',
  ALREADY_EXISTS = 'ALREADY_EXISTS',
  RESOURCE_LOCKED = 'RESOURCE_LOCKED',

  // Database errors (500)
  DB_CONNECTION = 'DB_CONNECTION',
  DB_QUERY_FAILED = 'DB_QUERY_FAILED',
  TRANSACTION_FAILED = 'TRANSACTION_FAILED',
}

/**
 * Helper function to handle unknown errors
 */
export function handleUnknownError(error: unknown): AppError {
  if (error instanceof AppError) {
    return error
  }

  if (error instanceof Error) {
    return new AppError(error.message, 500, 'UNKNOWN_ERROR', false)
  }

  return new AppError('An unknown error occurred', 500, 'UNKNOWN_ERROR', false)
}

/**
 * Type guard to check if error is operational
 */
export function isOperationalError(error: Error): boolean {
  if (error instanceof AppError) {
    return error.isOperational
  }
  return false
}

/**
 * Format error for client response
 */
export function formatErrorResponse(error: AppError): {
  success: false
  error: {
    message: string
    code: string
    statusCode: number
  }
} {
  return {
    success: false,
    error: {
      message: error.message,
      code: error.code,
      statusCode: error.statusCode,
    },
  }
}
