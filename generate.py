import git
import time
import os
import datetime
import subprocess
import dateutil.parser


def get_datetime_from_commit(c):
    ms_from_epoch = c.committed_date
    struct_time = time.gmtime(ms_from_epoch)
    return datetime.datetime(*struct_time[:-3])


def get_hexsha(c):
    return c.hexsha[:4]


def test_repo():
    new_path = os.path.join("dummy")
    import shutil
    shutil.rmtree(new_path, True)
    os.makedirs(new_path)
    r = git.Repo.init(new_path)
    return r


def new_date():
    return datetime.datetime.utcnow()


def days_from(n, date=None):
    if date is None:
        d = {"year": 2012, "day": 1, "month": 4}
        date = new_date().replace(**d)
    return date + datetime.timedelta(days=n)


def add_commit_to(r, n):
    directory = r.working_dir
    date = days_from(n)
    args = ["git", "commit", "-m", "heybro", "--allow-empty"]
    env = {}
    env["GIT_AUTHOR_DATE"] = date.isoformat()
    env["GIT_COMMITTER_DATE"] = date.isoformat()
    process = subprocess.Popen(args,
                               cwd=directory,
                               env=env,
                               stdout=subprocess.PIPE)
    return process.wait()


def add_commit_with_date(r, date, author=None, email=None):
    directory = r.working_dir
    args = ["git", "commit", "-m", "heybro", "--allow-empty"]
    env = {}
    env["GIT_AUTHOR_DATE"] = date.isoformat()
    env["GIT_COMMITTER_DATE"] = date.isoformat()
    if author is not None:
        env["GIT_AUTHOR_NAME"] = author
        env["GIT_COMMITTER_NAME"] = author
    if email is not None:
        env["GIT_AUTHOR_EMAIL"] = email
        env["GIT_COMMITTER_EMAIL"] = email
    process = subprocess.Popen(args,
                               cwd=directory,
                               env=env,
                               stdout=subprocess.PIPE)
    return process.wait()


def print_dates(r):
    com = r.iter_commits()
    com = list(com)
    for c in com:
        print get_hexsha(c), get_datetime_from_commit(c), c.message.strip()


def generate(r, iso_date, painted,
             author=None, email=None):
    date = dateutil.parser.parse(iso_date)
    for i in range(len(painted)):
        for times in range(painted[i]):
            current_date = days_from(i, date)
            add_commit_with_date(r, current_date, author=author,
                                 email=email)


if __name__ == '__main__':
    repo = test_repo()
    date = "2012-04-01T06:00:00.000Z"
    painted = [1, 0, 1, 0, 0, 2, 0]
    generate(repo, date, painted)
