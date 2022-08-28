import numpy
import datetime as dt


def init_date_table(library: list) -> list:
	date_table = []
	
	for work in library:
		if work['date'] != None:
			date_table.append(work['date'])
	
	return date_table


def init_graph(date_table: list) -> tuple:
	oldest = min(date_table)
	newest = max(date_table)
	
	x = range((newest - oldest).days + 1)
	y = [0] * len(x)
	
	for message in date_table:
		date = (message - oldest).days
		y[date] += 1
	
	return (x, y)


# Turn values corresponding to ticks into offsets from start
def pretty_labels(start: dt.datetime, ticks: list, values) -> list:
	labels = []

	for i in ticks:
		offset = dt.timedelta(days = int(values[i]))
		day = start + offset
		label = day.strftime("%d/%m/%Y")

		labels.append(label)
	
	return labels


def equispaced_ticks(start: dt.datetime, values, div: int = 15) -> tuple:
	step = len(values) // div
	ticks = range(0, len(values), step)

	return ticks


def oldest_work(library: list) -> dt.datetime:
	date_table = init_date_table(library)
	return min(date_table)


def graph_by_time(library: list) -> tuple:
	date_table = init_date_table(library)
	(x, y) = init_graph(date_table)

	return (numpy.array(x), numpy.array(y))

	
def polynomial_fit(graph, deg: int) -> tuple:
	if deg < 0:
		return (graph, None)
	
	(x, y) = graph
	fit = numpy.polyfit(x, y, deg)
	graph = (x, numpy.polyval(fit, x))
	
	return (graph, fit)


def minmax_ticks(start: dt.datetime, values, fit) -> tuple:
	d = numpy.polyder(fit)
	roots = numpy.roots(d)
	
	ticks = []
	for root in roots:
		if not numpy.iscomplex(root) and root >= values[0] and root <= values[-1]:
			root = numpy.real(root)
			ticks.append(int(root))

	return ticks
