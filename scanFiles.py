import os
import glob


def unique(a_list):
    return dict.fromkeys(a_list).keys()


def recursive_dirs(root):
    return filter((lambda a: a.rfind("CVS") == -1), [a[0] for a in os.walk(root)])


def scan_files(a_dir, accept=None, reject=None):
    if reject is None:
        reject = []
    if accept is None:
        accept = ["include"]
    sources = []
    paths = recursive_dirs(a_dir)
    for path in paths:
        for pattern in accept:
            sources += glob.glob(path + "/" + pattern)
    for pattern in reject:
        sources = filter((lambda a: a.rfind(pattern) == -1), sources)
    return list(unique(sources))
