#!/usr/bin/env python3.6
"""

"""

from socket import socket, SOL_SOCKET, SO_REUSEADDR
from ssl import wrap_socket
from pathlib import Path
from sys import stderr, exit
from asyncio import (
    get_event_loop, start_server, open_connection, ensure_future,
    wait, FIRST_COMPLETED,
)
from functools import partial

cert_file = Path.home() / '.tlswrapper.pem'


async def client_connected(client_reader, client_writer, upstream, reverse):
	sock = socket()
	sock.connect(upstream)
	
	if reverse:
		sock = wrap_socket(sock, certfile=cert_file)

	upstream_reader, upstream_writer = await open_connection(
		sock=sock,
	)
	
	up_recv = None
	cl_recv = None
	while True:
		if up_recv is None:
			up_recv = ensure_future(upstream_reader.read(4096))
		
		if cl_recv is None:
			cl_recv = ensure_future(client_reader.read(4096))
		
		done, pending = await wait(
			[up_recv, cl_recv],
			return_when=FIRST_COMPLETED,
		)
		

		if up_recv in done:
			if up_recv.exception() is not None:
				break

			data = up_recv.result()
			client_writer.write(data)
			await client_writer.drain()
			up_recv = None

		if cl_recv in done:
			if cl_recv.exception() is not None:
				break

			data = cl_recv.result()
			upstream_writer.write(data)
			await upstream_writer.drain()
			cl_recv = None


async def main(upstream, bind, reverse):
	if not cert_file.exists():
		print(f"Certificate file ({cert_file}) doesn't exist", file=stderr)
		print()
		print(f'Create it with:')
		print(f'  openssl req -new -x509 \\')
		print(f'    -keyout {cert_file} \\')
		print(f'    -out {cert_file} \\')
		print(f'    -days 365 -nodes')
		print()
		exit(1)
	
	sock = socket()
	sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sock.bind(bind)
	sock.listen()
	
	if not reverse:
		sock = wrap_socket(sock, certfile=cert_file, server_side=True)
	
	print(f'Listening at {bind[0]}:{bind[1]}')
	
	server = await start_server(
	    partial(client_connected, upstream=upstream, reverse=reverse),
	    sock=sock,
	)
	await server.wait_closed()


def cli():
	def host_port_pair(s):
		host, port = s.split(':')
		return (host, int(port))
	
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', dest='upstream', required=True,
	    type=host_port_pair)
	parser.add_argument('-b', dest='bind', default=('127.0.0.1', 4443),
	    type=host_port_pair)
	parser.add_argument('-r', dest='reverse', action='store_true')
	args = parser.parse_args()
	
	loop = get_event_loop()
	loop.run_until_complete(main(**vars(args)))
	loop.close()


if __name__ == '__main__':
	cli()
