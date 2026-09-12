import atexit
import json
import os

from trace_client import TraceClient

#  @author Daniel McCoy Stephenson
#  @since September 11th, 2026

APPLICATION = "patchwork"
SETTINGS_FILE = "settings.json"
SETTINGS_SECTION = "usage_reporting"
DEFAULT_ENDPOINT = "https://trace.danielstephenson.dev"
DEFAULT_KEY = "LI4sklsyL-L1AXPQmBpgC5eI2H1jeYBUHavpuVdCGME"
VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt")

FIRST_RUN_NOTICE = (
    "Usage reporting is on: patchwork sends a startup event (program name and version only) "
    "to trace.danielstephenson.dev. "
    'Turn it off with "usage_reporting": {"enabled": false} in settings.json.'
)


def defaultSettings():
    """The usage_reporting block written to settings.json on first run."""
    return {"enabled": True, "endpoint": DEFAULT_ENDPOINT, "key": DEFAULT_KEY}


def readVersion(versionFile=VERSION_FILE):
    """The program's own version, as recorded in version.txt, or None if it cannot be read."""
    try:
        with open(versionFile, "r") as f:
            version = f.read().strip()
        return version or None
    except OSError:
        return None


def loadSettings(settingsFile=SETTINGS_FILE, log=print):
    """
    Read the usage_reporting block from the settings file, writing the default
    block (and printing the one-time notice) when the file does not have one yet.

    Returns:
        dict or None: The usage_reporting settings, or None if the settings file
        exists but cannot be read, in which case nothing should be reported.
    """
    settings = {}
    if os.path.exists(settingsFile):
        try:
            with open(settingsFile, "r") as f:
                settings = json.load(f)
            if not isinstance(settings, dict):
                raise ValueError("settings file is not a JSON object")
        except (OSError, ValueError) as e:
            log(f"Could not read {settingsFile} ({e}); usage reporting is off until it is fixed.")
            return None

    section = settings.get(SETTINGS_SECTION)
    if isinstance(section, dict):
        return section

    settings[SETTINGS_SECTION] = defaultSettings()
    log(FIRST_RUN_NOTICE)
    try:
        with open(settingsFile, "w") as f:
            json.dump(settings, f, indent=2)
    except OSError as e:
        log(f"Could not write {settingsFile} ({e}); the notice above will be shown again next time.")
    return settings[SETTINGS_SECTION]


def buildClient(section):
    """A TraceClient for the given usage_reporting settings; disabled when they are None or opted out."""
    if section is None:
        return TraceClient.disabled()
    enabled = section.get("enabled", True)
    endpoint = section.get("endpoint") or DEFAULT_ENDPOINT
    key = section.get("key") or DEFAULT_KEY
    try:
        return TraceClient(endpoint, APPLICATION, key=key, enabled=bool(enabled))
    except Exception:
        return TraceClient.disabled()


def startUsageReporting(settingsFile=SETTINGS_FILE, log=print):
    """
    Read the settings, build the client and report the startup event.
    Never raises; the client is closed automatically when the interpreter exits.

    Returns:
        TraceClient: The client, so that further events could be reported.
    """
    try:
        client = buildClient(loadSettings(settingsFile, log))
    except Exception:
        return TraceClient.disabled()
    version = readVersion()
    client.report("startup", tags={"version": version} if version else None)
    atexit.register(client.close)
    return client
