import git
import time
import os
import datetime
import calendar
import subprocess


def get_datetime_from_commit(c):
    ms_from_epoch = c.committed_date
    struct_time = time.gmtime(ms_from_epoch)
    return datetime.datetime(*struct_time[:-3])


def get_hexsha(c):
    return c.hexsha[:4]


def ms_of(dt):
    struct_time = dt.timetuple()
    return calendar.timegm(struct_time)


def set_date_to(c, n):
    dt = get_datetime_from_commit(c)
    dt = dt.replace(day=n)
    c.committed_date = ms_of(dt)
    c.authored_date = ms_of(dt)
    c.message = c.message + "modified" + str(time.time())


def test_repo():
    new_path = os.path.join("dummy", "repoh")
    import shutil
    shutil.rmtree(new_path, True)
    os.makedirs(new_path)
    r = git.Repo.init(new_path)
    return r


def new_date():
    return datetime.datetime.utcnow()


def dirty_change_date_to(repo, commit_sha, datetime_obj):
    return subprocess.Popen(['git filter-branch --env-filter',
                             filter_script_change_date(commit_sha,
                                                       datetime_obj)],
                            cwd=repo.working_dir, shell=True)


def filter_script_change_date(commit_sha, datetime_obj):
    filter_template = ("if [ $GIT_COMMIT = {sha} ]; "
                       "then "
                       "export GIT_AUTHOR_DATE=\"{date}\"; "
                       "export GIT_COMMITTER_DATE=\"{date}\"; "
                       "fi")
    iso_date = datetime_obj.isoformat()
    return filter_template.format(sha=commit_sha, date=iso_date)


def change_date_to(repo, commit_sha, datetime_obj, first_commit=False):
    print "changing", commit_sha[:4]
    git_fn = repo.git
    args = ["-f", "--env-filter"]
    filter_script = filter_script_change_date(commit_sha, datetime_obj)
    args.append(filter_script)
    if not first_commit:
        args.append(commit_sha + "^..HEAD")
    return git_fn.filter_branch(args)


def generate_and_filter_branch(r):
    index = r.index
    for i in range(60):
        c = index.commit("derp " + str(i))

    index.write()

    print_dates(r)
    print "."

    shas = [c.hexsha for c in r.iter_commits()]
    shas = shas
    date_data = {"year": 2012, "month": 4, "day": 1}
    start_day = new_date().replace(**date_data)
    dates = []

    for i in range(len(shas)):
        dates.append(start_day + datetime.timedelta(hours=i))

    # hits newest commit first, so have dates mirror that
    dates = list(reversed(dates))

    for commit, date in zip(shas, dates)[:-1]:
        change_date_to(r, commit, date)
    change_date_to(r, shas[-1], dates[-1], True)  # last one's special

    print_dates(r)


def print_dates(r):
    com = r.iter_commits()
    com = list(com)
    for c in com:
        print get_hexsha(c), get_datetime_from_commit(c), c.message.strip()


def generate_and_set_stuff_after(r):
    index = r.index
    for i in range(10):
        c = index.commit("first")
        set_date_to(c, i + 1)

    index.write()

    print_dates(r)

if __name__ == '__main__':
    repo = test_repo()
    generate_and_filter_branch(repo)
