#!/usr/bin/env python3
"""
Native messaging host for ChatGPT Atlas Opener Chrome extension.
Receives URLs from the extension and opens them in ChatGPT Atlas.
"""

import sys
import json
import struct
import subprocess

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
    try:
        subprocess.run(
            ['open', '-a', 'ChatGPT Atlas', url],
            check=True,
            capture_output=True,
            text=True
        )
        return {'success': True}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

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
