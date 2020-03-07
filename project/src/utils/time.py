from pytz import timezone as tzone
from datetime import datetime, timezone


class TimeUtil(object):

    PST = tzone('US/Pacific')

    @staticmethod
    def get_current_time():
        '''
        Util method to get the time. Import this object
        and use it so that we don't have to manually configure time.\n
        @author npcompletenate
        '''
        utc_dt = datetime.now(timezone.utc)
        return utc_dt.astimezone(TimeUtil.PST).isoformat()
