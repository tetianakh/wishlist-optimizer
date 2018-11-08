from wishlist_optimizer.models import Language


class LanguagesService:
    def get_all_languages(self):
        return [l.name for l in Language.query.all()]

    def get_language_mkm_ids(self):
        return {l.name: l.mkm_id for l in Language.query.all()}

    def find_by_name(self, names):
        result = (
            Language.query.filter_by(name=name).first()
            for name in set(names)
        )
        return [l for l in result if l]
