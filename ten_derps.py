import git
import time
import os
import datetime
import calendar


def get_datetime_from_commit(c):
    ms_from_epoch = c.committed_date
    struct_time = time.gmtime(ms_from_epoch)
    return datetime.datetime(*struct_time[:-3])


def ms_of(dt):
    struct_time = dt.timetuple()
    return calendar.timegm(struct_time)


def set_hour_to(c, n):
    dt = get_datetime_from_commit(c)
    dt = dt.replace(hour=n)
    c.committed_date = ms_of(dt)


new_path = os.path.join("dummy", str(time.time()))
os.makedirs(new_path)
r = git.Repo.init(new_path)
index = r.index
for i in range(10):
    index.commit("derp")

index.write()

com = r.iter_commits()
com = list(com)
for c in com:
    print get_datetime_from_commit(c)

for c, n in zip(com, range(len(com))):
    set_hour_to(c, n)

for c in com:
    print get_datetime_from_commit(c)
