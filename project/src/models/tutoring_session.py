class TutoringSession:
    """
    Holds information about tutor sessions for stats.
    Fields:
    start --> start time of session
    end --> end time of session
    duration --> duration of session
    time_helping --> time grader spent resolving tickets during session
    utlization --> time_helping / duration
    accepted --> number of tickets accepted during session
    resolved --> number of tickets resolved during session
    """
    def __init__(self, start, end, duration, time_helping, utilization,
                 accepted, resolved):
        self.start = start
        self.end = end
        self.duration = duration
        self.time_helping = time_helping
        self.utilization = utilization
        self.accepted = accepted
        self.resolved = resolved
