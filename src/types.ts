export type TokenPayload<
  T extends Record<string, unknown> = Record<string, unknown>,
> = {
  token: string
  payload: T
}

export type TokenProvider<
  T extends Record<string, unknown> = Record<string, unknown>,
> = (...args: any[]) => Promise<TokenPayload<T> | null>
