def turkish_chars_to_ascii_chars(turkish_string):
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü']
    latin_chars = ['c', 'g', 'i', 'o', 's', 'u']

    cleared_str = ''
    for s in turkish_string:
        try:
            index_of_ascii_char = turkish_chars.index(s)
            cleared_str += latin_chars[index_of_ascii_char]
        except ValueError:
            # means that: it is not a special Turkish char
            cleared_str += s
    return cleared_str
