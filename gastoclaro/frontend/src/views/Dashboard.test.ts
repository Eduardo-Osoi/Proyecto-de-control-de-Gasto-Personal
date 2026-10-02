import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from './Dashboard.vue'
import api from '../api'

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() }),
}))

vi.mock('../api', () => ({
  default: { get: vi.fn(), post: vi.fn(), delete: vi.fn() },
}))

describe('Dashboard.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.mocked(api.get).mockReset()
  })

  it('muestra el skeleton mientras carga y el contenido cuando termina', async () => {
    let resolverCats: (v: any) => void = () => {}
    vi.mocked(api.get).mockImplementation((url: string) => {
      if (url === '/categorias/') return new Promise((r) => { resolverCats = r })
      return Promise.resolve({ data: [] })
    })

    const wrapper = mount(Dashboard)

    expect(wrapper.find('[data-testid="skeleton"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="contenido"]').exists()).toBe(false)

    resolverCats({ data: [] })
    await flushPromises()

    expect(wrapper.find('[data-testid="skeleton"]').exists()).toBe(false)
    expect(wrapper.find('[data-testid="contenido"]').exists()).toBe(true)
  })

  it('quita el skeleton incluso si la carga falla', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('falló la red'))

    const wrapper = mount(Dashboard)
    await flushPromises()

    expect(wrapper.find('[data-testid="skeleton"]').exists()).toBe(false)
    expect(wrapper.text()).toContain('No se pudo cargar la información')
  })

  it('calcula el total sumando los montos de los gastos', async () => {
    vi.mocked(api.get).mockImplementation((url: string) => {
      if (url === '/gastos/') {
        return Promise.resolve({
          data: [
            { id: 1, descripcion: 'Tacos', monto: 150, fecha: '2026-01-01', categoria_id: 1 },
            { id: 2, descripcion: 'Café', monto: 50.5, fecha: '2026-01-02', categoria_id: 1 },
          ],
        })
      }
      return Promise.resolve({ data: [] })
    })

    const wrapper = mount(Dashboard)
    await flushPromises()

    expect(wrapper.find('.cifra').text()).toBe('$200.50')
  })
})
