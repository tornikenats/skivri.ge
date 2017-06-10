import os

month_geo_to_eng = {
    'იანვარი'   :'January',
    'თებერვალი' :'February',
    'მარტი'     :'March',
    'აპრილი'    :'April',
    'მაისი'     :'May',
    'ივნისი'    :'June',
    'ივლისი'    :'July',
    'აგვისტო'   :'August',
    'სექტემბერი':'September',
    'ოქტომბერი' :'October',
    'ნოემბერი'  :'November',
    'დეკემბერი' :'December',
}

letter_map_geo_eng = {
    'ა': 'a',
    'ბ': 'b',
    'გ': 'g',
    'დ': 'd',
    'ე': 'e',
    'ვ': 'v',
    'ზ': 'z',
    'თ': 't',
    'ი': 'i',
    'კ': 'k',
    'ლ': 'l',
    'მ': 'm',
    'ნ': 'n',
    'ო': 'o',
    'პ': 'p',
    'ჟ': 'zh',
    'რ': 'r',
    'ს': 's',
    'ტ': 't',
    'უ': 'u',
    'ფ': 'f',
    'ქ': 'q',
    'ღ': 'gh',
    'ყ': 'k',
    'შ': 'sh',
    'ჩ': 'ch',
    'ც': 'c',
    'ძ': 'dz',
    'წ': 'ts',
    'ჭ': 'ch',
    'ხ': 'kh',
    'ჯ': 'j',
    'ჰ': 'h',
}


def direct_translate(str):
    return ''.join(letter_map_geo_eng.get(ch, ch) for ch in str)

def get_debug_flag(default=None):
    val = os.environ.get('SKIVRIGE_SCRAPER_DEBUG')
    if not val:
        return default
    return val not in ('0', 'false', 'no')