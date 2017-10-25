class StatisticTableViewModel:
    def __init__(self, result_set, *exclude_fields, title=None):

        # Get the first result for getting general race_info in order to construct the table title
        first = result_set[0]
        if title:
            self.title = title
        else:
            self.title = "{0} meters, {1}".format(first.distance, first.track_type)
        self.rows = [s.get_pure_dict(*exclude_fields) for s
                     in
                     result_set]
        self.col_headers = self.prettify_keys(self.rows[0].keys())

    def prettify_keys(self, keys):
        _keys = list()
        for key in keys:
            # Split by the underscore
            words = key.split('_')
            # Capitalize the first letter of each word and build the string
            _key = ''
            for word in words:
                _key += word.title() + ' '

            # Add the key to the return list
            _keys.append(_key)
        return _keys
