const DRAFT = 'wishlist-draft'

class DraftStore {
  getDraft () {
    return JSON.parse(localStorage.getItem(DRAFT))
  }
  hasDraft () {
    const draft = this.getDraft()
    return !!draft && !!draft.cards && draft.cards.length > 0
  }
  setDraft (draft) {
    localStorage.setItem(DRAFT, JSON.stringify(draft))
  }
}

export default new DraftStore()
