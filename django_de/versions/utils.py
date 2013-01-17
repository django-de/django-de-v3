import requests
import logging

from django.core.cache import cache
from django.conf import settings


LOG = logging.getLogger(__name__)


def is_prerelease(version_str):
    """
    Checks if the given version_str represents a prerelease version.
    """
    return any([c.isalpha() for c in version_str])


def get_version_data(force=False):
    """
    Fetches the latest version info from the Github API url specified
    with VERSIONS_API_URL and returns a tuple of latest_stable and
    latest_prerelease.

    Note that this implementation caches the result with VERSIONS_CACHE_TIMEOUT.
    """
    latest_stable = None
    latest_pre = None
    cache_key = 'versioninfo'
    api_url = getattr(settings, 'VERSIONS_API_URL',
        'https://api.github.com/repos/django/django/git/refs/tags')
    cache_duration = getattr(settings, 'VERSIONS_CACHE_TIMEOUT', 3600)

    if not force:
        info = cache.get(cache_key)
        if info is not None:
            LOG.debug("Found versioninfo in cache")
            return info
        LOG.debug("Couldn't find versioninfo in cache. Refetching...")

    try:
        data = requests.get(api_url).json()
    except:
        LOG.exception("Failed to fetch versinfo data")
        return None

    for tag in data:
        tag_name = tag['ref'].split('/')[-1]
        if is_prerelease(tag_name):
            latest_pre = tag_name
        else:
            latest_stable = tag_name
    info = (latest_stable, latest_pre)
    cache.set(cache_key, info, cache_duration)
    return info
