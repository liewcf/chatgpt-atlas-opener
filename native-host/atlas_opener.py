#!/usr/bin/env python3
"""
Native messaging host for ChatGPT Atlas Opener Chrome extension.
Receives URLs from the extension and opens them in ChatGPT Atlas.
"""

import sys
import json
import struct
import subprocess
import time

ATLAS_APP_NAME = "ChatGPT Atlas"
ATLAS_BUNDLE_ID = "com.openai.atlas"
ATLAS_STARTUP_TIMEOUT = 10  # seconds to wait for the app to finish launching
ATLAS_STARTUP_POLL_INTERVAL = 0.5  # seconds between checks
ATLAS_READY_DELAY = 1.5  # seconds to allow Atlas to register URL handlers after launch
ATLAS_OPEN_RETRIES = 5  # attempts to deliver the URL once Atlas is running

def send_message(message):
    """Send a message to the Chrome extension."""
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def read_message():
    """Read a message from the Chrome extension."""
    text_length_bytes = sys.stdin.buffer.read(4)
    if len(text_length_bytes) == 0:
        return None
    
    text_length = struct.unpack('I', text_length_bytes)[0]
    text = sys.stdin.buffer.read(text_length).decode('utf-8')
    return json.loads(text)

def open_in_atlas(url):
    """Open URL in ChatGPT Atlas using macOS open command."""
    launch_error = ensure_atlas_running()
    if launch_error:
        return launch_error

    time.sleep(ATLAS_READY_DELAY)

    last_error = "Unknown error"
    for attempt in range(ATLAS_OPEN_RETRIES):
        delivery_error = deliver_url_to_atlas(url)
        if delivery_error is None:
            return {'success': True}

        last_error = delivery_error

        if attempt < ATLAS_OPEN_RETRIES - 1 and not is_atlas_running():
            relaunch_error = ensure_atlas_running()
            if relaunch_error:
                return relaunch_error

        time.sleep(ATLAS_STARTUP_POLL_INTERVAL * (attempt + 1))

    return {'success': False, 'error': last_error}

def ensure_atlas_running():
    """
    Launch ChatGPT Atlas if it is not already running.
    Waits until the process is detected or times out.
    """
    if is_atlas_running():
        return None

    try:
        # Launch the app without a URL so it can finish booting
        subprocess.run(
            ['open', '-b', ATLAS_BUNDLE_ID],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as error:
        return {'success': False, 'error': f'Unable to launch {ATLAS_APP_NAME}: {format_subprocess_error(error)}'}
    except Exception as error:
        return {'success': False, 'error': f'Unexpected error launching {ATLAS_APP_NAME}: {error}'}

    deadline = time.time() + ATLAS_STARTUP_TIMEOUT
    while time.time() < deadline:
        if is_atlas_running():
            # Give the app a moment to become fully responsive
            time.sleep(ATLAS_STARTUP_POLL_INTERVAL)
            return None
        time.sleep(ATLAS_STARTUP_POLL_INTERVAL)

    return {'success': False, 'error': f'{ATLAS_APP_NAME} did not finish launching within {ATLAS_STARTUP_TIMEOUT} seconds'}

def is_atlas_running():
    """Check if ChatGPT Atlas is currently running."""
    script = 'tell application "System Events" to exists (process "{}")'.format(ATLAS_APP_NAME)

    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().lower() == 'true'
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

def deliver_url_to_atlas(url):
    """Send the URL to ChatGPT Atlas via AppleScript."""
    script = 'tell application "{}" to open location "{}"'.format(
        ATLAS_APP_NAME,
        escape_apple_script_string(url)
    )

    try:
        subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return None
    except subprocess.CalledProcessError as error:
        return format_subprocess_error(error)
    except Exception as error:
        return str(error)

def escape_apple_script_string(value):
    """Escape backslashes and quotes for AppleScript string literals."""
    return value.replace("\\", "\\\\").replace('"', '\\"')

def format_subprocess_error(error):
    """Return a helpful error message from a subprocess.CalledProcessError."""
    stderr = (error.stderr or "").strip()
    stdout = (error.stdout or "").strip()
    details = stderr or stdout or str(error)
    return details or f'Command failed with exit code {error.returncode}'

def main():
    while True:
        message = read_message()
        if message is None:
            break
        
        if 'url' in message:
            response = open_in_atlas(message['url'])
            send_message(response)
        else:
            send_message({'success': False, 'error': 'No URL provided'})

if __name__ == '__main__':
    main()
