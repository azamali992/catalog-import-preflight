import argparse,http.server,pathlib,functools
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8013);p.add_argument('--reset',action='store_true');a=p.parse_args()
print('Stateless demo: every page reload resets all selections. No persistent customer data.')
http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))).serve_forever()
