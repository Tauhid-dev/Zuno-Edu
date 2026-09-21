"""ASGI entrypoint; composition remains in bootstrap."""

from zuno_edu.bootstrap.app import create_app

app = create_app()
