import { defineStore } from 'pinia'

// uso sessionStorage y no localStorage para que el token no sobreviva
// entre pestañas ni se quede pegado si hay XSS
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem('gastoclaro_token') as string | null,
    usuario: null as { id: number; email: string; nombre: string } | null,
  }),
  actions: {
    setSesion(token: string) {
      this.token = token
      sessionStorage.setItem('gastoclaro_token', token)
    },
    setUsuario(usuario: { id: number; email: string; nombre: string }) {
      this.usuario = usuario
    },
    cerrarSesion() {
      this.token = null
      this.usuario = null
      sessionStorage.removeItem('gastoclaro_token')
    },
  },
})
