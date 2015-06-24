"""dockermon testing"""

import dockermon


def test_http_status():
    header = 'HTTP/1.1 200 Okie Dokie\r'
    parsed = dockermon.header_status(header)
    assert parsed == (200, 'Okie Dokie')


def test_read_http_header():
    pass  # TBD


def test_watch():
    pass  # TBD


def test_print_callback():
    pass


def test_prog_callback():
    pass  # TBD


def test_main():
    pass  # TBD
