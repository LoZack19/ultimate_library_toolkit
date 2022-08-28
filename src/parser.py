import json
import re
from src import fdate

class Splitter:

    @staticmethod
    def split(clear: tuple) -> dict:
        raw_work = {}
        keys = ["author", "date", "nation", "place"]
        pattern = r",|-|\[|\]"

        (title, rest) = clear[0].split('⏺')
        link = clear[1]

        fields = re.split(pattern, rest)
        fields.pop(-1)

        for (i, key) in enumerate(keys):
            raw_work[key] = fields[i].strip()
        
        raw_work["title"] = title.strip()
        raw_work["link"] = link
        
        return raw_work


class Resolver:

    def __init__(self, files):
        self.adjustments = self.init_adjustments(files)

    @staticmethod
    def init_adjustments(files: dict) -> dict:
        adjustments = {}
        
        for file in files:
            with open(files[file], 'r') as infile:
                adjustment = json.load(infile)
            
            adjustments[file] = adjustment
        
        return adjustments
    

    @staticmethod
    def field_to_key(field: str) -> str:
        return field + 's'
    

    def get_adjustment(self, field: str) -> dict:
        key = self.field_to_key(field)
        return self.adjustments[key]
    

    def resolve_field(self, field: str, value):
        res = value
        adjustment = self.get_adjustment(field)
        
        for sub in adjustment:
            if value in adjustment[sub]:
                res = sub
        
        return res


    def resolve_work(self, raw_work: dict) -> dict:
        work = dict(raw_work)

        for field in work:
            adjustment = self.adjustments[field + 's']
            for sub in adjustment:
                if work[field] in adjustment[sub]:
                    work[field] = sub
        
        return work
    

    def resolve_lib(self, raw_library: list, fields: list = None) -> list:
        library = []

        for raw_work in raw_library:
            work = self.resolve_work(raw_work, fields)
            library.append(work)
        
        return library


def parse(clears: list, files: dict, verbose=False) -> list:
    raw_works = []

    for clear in clears:
        try:
            raw_work = Splitter.split(clear)
            raw_works.append(raw_work)
        except ValueError:
            if verbose:
                print("[ERROR] Failed parsing of:", clear)
    
    works = []
    adj = Resolver(files)

    for raw_work in raw_works:
        work = adj.resolve_work(raw_work)
        try:
            work["date"] = fdate.text_to_datetime(work["date"])
        except ValueError:
            print("[ERROR] Message couldn't be parsed correctly:", work)
        works.append(work)

    return works