import logging
import netrc
import os
from pathlib import Path
from platform import system
from typing import List, Tuple

import asf_search
from hyp3lib.get_orb import downloadSentinelOrbitFile


log = logging.getLogger(__name__)
ESA_HOST = 'dataspace.copernicus.eu'
EARTHDATA_HOST = 'urs.earthdata.nasa.gov'


def get_netrc():
    netrc_name = '_netrc' if system().lower() == 'windows' else '.netrc'
    netrc_file = Path.home() / netrc_name
    return netrc_file


def find_creds_in_env(username_name, password_name):
    if username_name in os.environ and password_name in os.environ:
        username = os.environ[username_name]
        password = os.environ[password_name]
        return username, password

    return None, None


def find_creds_in_netrc(host):
    netrc_file = get_netrc()
    if netrc_file.exists():
        netrc_credentials = netrc.netrc(netrc_file)
        if host in netrc_credentials.hosts:
            username = netrc_credentials.hosts[host][0]
            password = netrc_credentials.hosts[host][2]
            return username, password

    return None, None


def get_esa_credentials() -> Tuple[str, str]:
    username, password = find_creds_in_env('ESA_USERNAME', 'ESA_PASSWORD')
    if username and password:
        return username, password

    username, password = find_creds_in_netrc(ESA_HOST)
    if username and password:
        return username, password

    raise ValueError(
        'Please provide Copernicus Data Space Ecosystem (CDSE) credentials via the '
        'ESA_USERNAME and ESA_PASSWORD environment variables, or your netrc file.'
    )


def get_earthdata_credentials() -> Tuple[str, str]:
    username, password = find_creds_in_env('EARTHDATA_USERNAME', 'EARTHDATA_PASSWORD')
    if username and password:
        return username, password

    username, password = find_creds_in_netrc(EARTHDATA_HOST)
    if username and password:
        return username, password

    raise ValueError(
        'Please provide NASA EarthData credentials via the '
        'EARTHDATA_USERNAME and EARTHDATA_PASSWORD environment variables, or your netrc file.'
    )


def download_granule(granule_name: str, output_dir: Path):
    """Download a S1 granule using asf_search.

    Args:
        granule_name: Name of the granule to download
        output_dir: Directory to save the granule in
    """
    username, password = get_earthdata_credentials()
    session = asf_search.ASFSession().auth_with_creds(username, password)

    results = asf_search.granule_search([granule_name])
    results.download(path=output_dir, session=session)
    return output_dir / granule_name


def download_orbit(granule_name: str, output_dir: Path):
    """Download a S1 orbit file. Prefer using the ESA API,
    but fallback to ASF if needed.

    Args:
        granule_name: Name of the granule to download
        output_dir: Directory to save the orbit file in
    """
    orbit_path, _ = downloadSentinelOrbitFile(granule_name, str(output_dir), esa_credentials=get_esa_credentials())
    return orbit_path


def call_stanford_module(local_name, args: List = []):
    """Call a Stanford Processor modules (via subprocess) with the given arguments.

    Args:
        local_name: Name of the module to call (e.g. 'sentinel/sentinel_scene_cpu.py')
        args: List of arguments to pass to the module
    """
    proc_home = os.environ.get('PROC_HOME', None)
    if proc_home is None:
        raise ValueError('PROC_HOME environment variable is not set. Location of Stanford modules is unknown.')
    proc_home = Path(proc_home)
    log.info(f'Calling {local_name} with arguments: {" ".join(args)}')
    # TODO: Actually call the module via subprocess