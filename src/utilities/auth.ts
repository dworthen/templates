import * as jose from 'jose'

import { TokenProvider } from '../types'

export const cookieTokenProvider: TokenProvider =
  async function cookieTokenProvider(cookieName: string) {
    const cookie = await window.cookieStore.get(cookieName)
    if (cookie !== null) {
      const token = cookie.value
      const claims = jose.decodeJwt(token)
      return { token, payload: claims }
    }
    return null
  }

export const localStorageTokenProvider: TokenProvider =
  async function localStorageTokenProvider(key: string) {
    const token = localStorage.getItem(key)
    if (token != null) {
      const claims = jose.decodeJwt(token)
      return { token, payload: claims }
    }
    return null
  }
