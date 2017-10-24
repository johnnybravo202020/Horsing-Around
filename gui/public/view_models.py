class StatisticTableViewModel:
    def __init__(self, title, result_set):
        self.title = title
        self.rows = [s.get_pure_dict('id') for s in result_set]
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
