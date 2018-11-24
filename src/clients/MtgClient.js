import mtg from 'mtgsdk'

export default class MtgClient {
  getCards (searchTerm) {
    return mtg.card.where({'name': searchTerm})
  }
}
