const DRAFT = 'wishlist-draft'

class DraftStore {
  getDraft () {
    return JSON.parse(localStorage.getItem(DRAFT))
  }
  hasDraft () {
    return !!this.getDraft()
  }
  setDraft (draft) {
    localStorage.setItem(DRAFT, JSON.stringify(draft))
  }
}

export default new DraftStore()
