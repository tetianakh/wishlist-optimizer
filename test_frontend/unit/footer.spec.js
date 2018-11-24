import { expect } from 'chai'
import { shallowMount } from '@vue/test-utils'
import Footer from '@/components/Footer.vue'

describe('Footer.vue', () => {
  it('renders copyright message', () => {
    const wrapper = shallowMount(Footer)
    const currentYear = new Date().getFullYear()
    expect(wrapper.text()).to.include(`© Foki ${currentYear}`)
  })
  it('renders github message', () => {
    const wrapper = shallowMount(Footer)
    expect(wrapper.text()).to.include('Find us on github')
  })
})
