##TIME FEATURES
def timediff(t1, t2):
    """difference between times (millisec precision) as days"""
    return (t1-t2)/(86400.*1000)

def getProjectIntervals(projects):
    """List of intervals between consecutive projects"""
    intervals = []
    prev = projects[0]["**created"]
    for project in projects[1:]:
        curr = project['**created']
        intervals.append(timediff(curr, prev))
        prev = curr
    return numpy.array(intervals)

def getProjectLengths(projects):
    """Lengths (according to last modified date) of projects"""
    return numpy.array([timediff(project["**modified"], project["**created"]) for project in projects])

def numProjects(projects):
	return len(projects)

def numOnDay(projects):
    """number of projects per day of the week"""
    num_projs = len(projects)
    weekday_projs = 0
    dow = []
    for i in range(7):
        dow.append(0)
    for project in projects:
        date = datetime.datetime.fromtimestamp(project['**created'] / 1e3).weekday()
        dow[date] += 1.0
    return numpy.array(dow)

def percentOnWeekday(projectsdow):
    """percentage of projects on a weekday, given number of projects for each day"""
    return sum(projectsdow[:5]) / sum(projectsdow) * 100

def projectsPerUserPeriod(projects, bins=10):
    '''histogram of number of projects across user's lifespan'''
    first= projects[0]['**created']
    daysElapsed = [timediff(project['**created'], first) for project in projects]
    hist, _ = numpy.histogram(daysElapsed, bins=bins)
    return hist
