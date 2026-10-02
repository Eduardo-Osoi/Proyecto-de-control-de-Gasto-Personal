import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Login from './Login.vue'
import api from '../api'

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() }),
}))

vi.mock('../api', () => ({
  default: { get: vi.fn(), post: vi.fn() },
}))

const stubs = { RouterLink: { template: '<a><slot /></a>' } }

describe('Login.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.mocked(api.post).mockReset()
    vi.mocked(api.get).mockReset()
  })

  it('muestra el error que devuelve el backend si el login falla', async () => {
    vi.mocked(api.post).mockRejectedValueOnce({
      response: { data: { detail: 'Correo o contraseña incorrectos' } },
    })

    const wrapper = mount(Login, { global: { stubs } })
    await wrapper.find('input[type="email"]').setValue('ana@correo.com')
    await wrapper.find('input[type="password"]').setValue('mala')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('Correo o contraseña incorrectos')
  })

  it('pide el perfil después de un login exitoso', async () => {
    vi.mocked(api.post).mockResolvedValueOnce({ data: { access_token: 'tok-123' } })
    vi.mocked(api.get).mockResolvedValueOnce({ data: { id: 1, email: 'ana@correo.com', nombre: 'Ana' } })

    const wrapper = mount(Login, { global: { stubs } })
    await wrapper.find('input[type="email"]').setValue('ana@correo.com')
    await wrapper.find('input[type="password"]').setValue('clave1234')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(api.post).toHaveBeenCalledWith('/auth/login', { email: 'ana@correo.com', password: 'clave1234' })
    expect(api.get).toHaveBeenCalledWith('/auth/me')
  })

  it('desactiva el botón mientras está cargando', async () => {
    let resolver: (v: any) => void = () => {}
    vi.mocked(api.post).mockReturnValueOnce(new Promise((r) => { resolver = r }))

    const wrapper = mount(Login, { global: { stubs } })
    await wrapper.find('input[type="email"]').setValue('ana@correo.com')
    await wrapper.find('input[type="password"]').setValue('clave1234')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('button[type="submit"]').attributes('disabled')).toBeDefined()

    resolver({ data: { access_token: 'tok' } })
    await flushPromises()
  })
})
