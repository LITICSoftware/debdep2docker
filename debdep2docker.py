#! /usr/bin/env python
#
# Generate a Dockerfile to provide the dependecies from .deb package files.

import argparse
import subprocess

def query_deps(filename):
    """Query the Depend field of a .deb file"""
    cmd = ["dpkg-deb", "-f", filename, "Depends"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    return res.stdout.decode("utf-8")

def parse_deps(deps_str):
    """Extract list of package names from raw field string"""
    pkgs = []
    for dep in deps_str.split(','):
        dep = dep.strip()            # rm whitespace
        if dep:
            pkgs.append(dep.split()[0])  # ignore version req.
    return pkgs

def get_deps(filename):
    """List of packages from .deb files."""
    return parse_deps(query_deps(filename))

def merge_deps(depss):
    """Unique packages from list of lists"""
    uniq_pkgs = set()
    for lst in depss:
        uniq_pkgs.update(lst)
    return sorted(list(uniq_pkgs))


def main(filenames):
    pkgs = merge_deps([get_deps(f) for f in filenames])
    print(pkgs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("deb", nargs="+", help="Debian packages")
    args = parser.parse_args()

    main(args.deb)
