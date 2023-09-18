import requests

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse


URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_latest_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""
    res = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if res.status_code == requests.codes.ok:
        j = res.json()
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version

