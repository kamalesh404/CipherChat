"""CLI for CipherChat — keygen, register, chat."""

from __future__ import annotations

import json
import os

import click

from src.core.config import Config
from src.crypto.aes import decrypt, derive_key, encrypt
from src.crypto.keys import ecdh, generate_keypair, pub_from_priv


def _key_path(name: str) -> str:
    return os.path.join(".cipherchat", f"{name}.key")


@click.group()
def cli():
    """CipherChat — E2E encrypted chat."""


@cli.command()
@click.argument("username")
def keygen(username: str):
    """Generate X25519 keypair for USERNAME."""
    priv, pub = generate_keypair()
    os.makedirs(".cipherchat", exist_ok=True)
    with open(_key_path(username), "wb") as fh:
        fh.write(priv)
    click.echo(f"Keys for {username}:")
    click.echo(f"  priv: {_key_path(username)} (keep secret)")
    click.echo(f"  pub : {pub.hex()}")


@cli.command()
@click.argument("username")
@click.option("--host", default="http://127.0.0.1:8080")
def register(username: str, host: str):
    """Register USERNAME's public key on the server."""
    import urllib.request
    priv_path = _key_path(username)
    if not os.path.exists(priv_path):
        raise click.ClickException(f"No key for {username}. Run keygen first.")
    with open(priv_path, "rb") as fh:
        priv = fh.read()
    pub = pub_from_priv(priv).hex()
    data = json.dumps({"username": username, "public_key": pub}).encode()
    req = urllib.request.Request(f"{host}/v1/register", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        click.echo(resp.read().decode())


@cli.command()
@click.argument("username")
@click.argument("peer")
@click.argument("message")
def encrypt_msg(username: str, peer: str, message: str):
    """Encrypt MESSAGE from USERNAME to PEER (demo, no server)."""
    priv_path = _key_path(username)
    # For demo, derive peer pub via env or prompt — here we just need a pub hex
    peer_pub_hex = click.prompt(f"Peer {peer} pub hex")
    with open(priv_path, "rb") as fh:
        priv = fh.read()
    shared = ecdh(priv, bytes.fromhex(peer_pub_hex))
    key = derive_key(shared)
    ct = encrypt(key, message.encode()).hex()
    click.echo(ct)


@cli.command()
@click.argument("username")
@click.argument("peer")
@click.argument("cipher_hex")
def decrypt_msg(username: str, peer: str, cipher_hex: str):
    """Decrypt CIPHER_HEX for USERNAME from PEER."""
    priv_path = _key_path(username)
    peer_pub_hex = click.prompt(f"Peer {peer} pub hex")
    with open(priv_path, "rb") as fh:
        priv = fh.read()
    shared = ecdh(priv, bytes.fromhex(peer_pub_hex))
    key = derive_key(shared)
    pt = decrypt(key, bytes.fromhex(cipher_hex))
    click.echo(pt.decode())


@cli.command()
def serve():
    """Start the server."""
    from src.api.server import main
    main()


if __name__ == "__main__":
    cli()
