
class ConditionService:
    # MT for Mint > NM for Near Mint > EX for Exellent > GD for Good >
    # LP for Light Played > PL for Played > PO for Poor
    CONDITIONS = {'MT', 'NM', 'EX', 'GD', 'LP', 'PL', 'PO'}
    DEFAULT = None

    def get_condition(self, card_data):
        if 'min_condition' not in card_data:
            return self.DEFAULT
        condition = str(card_data.get('min_condition')).upper()
        if condition not in self.CONDITIONS:
            return self.DEFAULT
        return condition
