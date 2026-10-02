import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from './auth'

describe('authStore', () => {
  beforeEach(() => {
    sessionStorage.clear()
    setActivePinia(createPinia())
  })

  it('arranca sin sesión si no hay nada en sessionStorage', () => {
    const auth = useAuthStore()
    expect(auth.token).toBeNull()
    expect(auth.usuario).toBeNull()
  })

  it('recupera el token de sessionStorage si ya había uno', () => {
    sessionStorage.setItem('gastoclaro_token', 'token-viejo')
    const auth = useAuthStore()
    expect(auth.token).toBe('token-viejo')
  })

  it('guarda el token al iniciar sesión', () => {
    const auth = useAuthStore()
    auth.setSesion('token-123')
    expect(auth.token).toBe('token-123')
    expect(sessionStorage.getItem('gastoclaro_token')).toBe('token-123')
  })

  it('limpia todo al cerrar sesión', () => {
    const auth = useAuthStore()
    auth.setSesion('token-123')
    auth.setUsuario({ id: 1, email: 'ana@correo.com', nombre: 'Ana' })

    auth.cerrarSesion()

    expect(auth.token).toBeNull()
    expect(auth.usuario).toBeNull()
    expect(sessionStorage.getItem('gastoclaro_token')).toBeNull()
  })
})
