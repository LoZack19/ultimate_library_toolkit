import datetime as dt


def text_to_datetime(date: str) -> dt.datetime:
    lookup = [
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre"
    ]

    if date == "None":
        return None

    (day, month, year) = date.split()
    month = lookup.index(month.lower()) + 1

    return dt.datetime(int(year), month, int(day))


def datetime_to_text(date: dt.datetime) -> str:
    strdate = 'None'
    
    lookup = [
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre"
    ]

    if date != None:
        (day, month, year) = (date.day, date.month, date.year)
        strdate = str(day) + ' ' + lookup[month - 1] + ' ' + str(year)
    
    return strdate


def stdstr_to_datetime(strdate: str) -> dt.datetime:
    date = None

    if strdate != 'None':
        strdate = strdate.split()[0]
        (year, month, day) = [int(s) for s in strdate.split('-')]
        date = dt.datetime(year, month, day)
    
    return date