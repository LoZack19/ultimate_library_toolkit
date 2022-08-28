from src.parser import Resolver
import json
import src.fdate as fdate
import src.scanner as scanner
import matplotlib.pyplot as plot
import datetime as dt


class Filter:

    @staticmethod
    # Return the works from the library whose value for the specified field matches the given value
    def filter(library: list, field: str, match: str) -> list:
        res = []

        for work in library:
            if work[field] == match:
                res.append(work)

        return res


class Shell:

    def __init__(self, general: list, files: dict):
        self.libraries = {"general": general}
        self.resolver = Resolver(files)
    

    # Load library from json file
    def load(self, filename: str, outlib: str):
        library = []

        with open(filename, 'r') as infile:
            library = json.load(infile)
        
        # Date string to datetime conversion
        for work in library:
            work["date"] = fdate.stdstr_to_datetime(work["date"])
        
        self.libraries[outlib] = library
    

    # Save library into json file
    def save(self, filename: str, inlib: str):
        library = self.libraries[inlib]

        for work in library:
            work["date"] = str(work["date"])

        with open(filename, 'w') as outfile:
            json.dump(library, fp=outfile, indent=4)
        
        # Restore dates
        for work in library:
            work["date"] = fdate.stdstr_to_datetime(work["date"])
    

    # Unite two libraries
    def or_(self, inlib1: str, inlib2: str, outlib: str):
        out = []

        for work in self.libraries[inlib1]:
            out.append(work)
        
        for work in self.libraries[inlib2]:
            if work not in out:
                out.append(work)
        
        self.libraries[outlib] = out
    
    
    # Intersect two libraries
    def and_(self, inlib1: str, inlib2: str, outlib: str):
        out = []

        for work in self.libraries[inlib1]:
            if work in self.libraries[inlib2]:
                out.append(work)
        
        self.libraries[outlib] = out
    

    # Complement a library
    def not_(self, inlib: str, outlib: str, universe: str = "general"):
        out = []

        for work in self.libraries[universe]:
            if work not in self.libraries[inlib]:
                out.append(work)
        
        self.libraries[outlib] = out
    

    # Print a library in BSL format
    def print_(self, inlib: str = "general"):
        library = self.libraries[inlib]

        for work in library:
            print("%s ⏺ %s, %s - %s [%s]" %
                (
                    work["title"],
                    work["author"],
                    fdate.datetime_to_text(work["date"]),
                    work["nation"],
                    work["place"]
                )
            )
    

    def list_(self):
        for library in self.libraries:
            print("- %s (%d)" % (library, len(self.libraries[library])))
    

    def del_(self, lib: str):
        self.libraries.pop(lib)
    

    # Select works which match a particular value for a given field
    def select(self, inlib: str, field: str, arg: str, outlib: str):
        library = self.libraries[inlib]
        match = self.resolver.resolve_field(field, arg)

        self.libraries[outlib] = Filter.filter(library, field, match)
    

    # Discard works which match a particular value for a given field
    def discard(self, inlib: str, field: str, arg: str, outlib: str):
        self.select(inlib, field, arg, "__tmp__")
        self.not_("__tmp__", outlib, inlib)
        self.del_("__tmp__")
    

    # Select works in a given time range
    def time_range(self, inlib: str, time_range: tuple, outlib: str):
        res = []

        library = self.libraries[inlib]
        (start, end) = time_range

        for work in library:
            if work["date"] != None and (start == None or start <= work["date"]) and (end == None or work["date"] <= end):
                res.append(work)
        
        self.libraries[outlib] = res
    

    def stat(self, inlib: str, field: str):
        library = self.libraries[inlib]
        counter = {}

        for work in library:
            if work[field] in counter:
                counter[work[field]] += 1
            else:
                counter[work[field]] = 1
        
        sorted_counter = sorted([(key, counter[key]) for key in counter], key=lambda x: x[1], reverse=True)

        for (key, value) in sorted_counter:
            print("%-12s : %3d" % (str(key), value))
    

    def plot(self, inlib: list = "general",
            deg: int = -1,              # Approximation degree (< 0 for none)
            plabels: str = 'pretty',    # Meaningful labels
            pticks = 'equispaced',      # Ticks position
            div: int = 15,              # [Only for equispaced ticks]
            show: bool = True,          # False to plot more graphs
            color: str = None           # Plot color
            ):
        
        library = self.libraries[inlib]

        start = scanner.oldest_work(library)
        graph = scanner.graph_by_time(library)
        (graph, fit) = scanner.polynomial_fit(graph, deg)

        (x, y) = graph

        (ticks, labels) = plot.xticks()
        if pticks == 'equispaced':
            ticks = scanner.equispaced_ticks(start, x, div)
        elif pticks == 'minmax' and deg > 0:
            ticks = scanner.minmax_ticks(start, x, fit)
            plot.scatter(ticks, [y[i] for i in ticks])
        
        if plabels == 'pretty':
            labels = scanner.pretty_labels(start, ticks, x)
        else:
            labels = [x[i] for i in ticks]
        
        plot.xticks(ticks = ticks,
                    labels = labels,
                    rotation = 45,
                    ha = 'right', rotation_mode = 'anchor')

        if color != None:
            plot.plot(x, y, color=color)
        else:
            plot.plot(x, y)

        if (show):
            plot.show()
    
    def save_graph(self, inlib: str, filename: str = None):
        library = self.libraries[inlib]

        if filename == None:
            filename = inlib + '_graph.dat'
        
        date_table = scanner.init_date_table(library)
        (x, y) = scanner.init_graph(date_table)
        del date_table

        with open(filename, 'w') as outfile:
            for i in range(len(x)):
                print("%d, %d" % (x[i], y[i]), file = outfile)