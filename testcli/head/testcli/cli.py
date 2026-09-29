import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import yaml


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _check(config):
    if not isinstance(config, dict):
        return "top-level document must be a mapping"
    if "name" not in config:
        return "field 'name' is required"
    return None


def _check_region(config):
    if "region" not in config:
        return "Missing region: field 'region' is required"
    return None


def cmd_validate(args):
    try:
        config = _load(args.file)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Invalid configuration: {exc}", file=sys.stderr)
        return 1
    error = _check(config)
    if error:
        print(f"Invalid configuration: {error}", file=sys.stderr)
        return 1
    region_error = _check_region(config)
    if region_error:
        print(region_error, file=sys.stderr)
        return 1
    print("Valid configuration")
    return 0


def cmd_convert(args):
    try:
        config = _load(args.file)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(config, indent=2, sort_keys=True))
    return 0


def cmd_inspect(args):
    try:
        config = _load(args.file)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if not isinstance(config, dict):
        print("Error: top-level document must be a mapping", file=sys.stderr)
        return 1
    for key in sorted(config):
        print(f"{key}: {type(config[key]).__name__}")
    return 0


def cmd_serve(args):
    try:
        body = json.dumps(_load(args.file)).encode("utf-8")
    except (OSError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Serving on http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="testcli", description="Sample config tool")
    sub = parser.add_subparsers(dest="command", metavar="{validate,convert,inspect,serve}")
    sub.required = True

    p = sub.add_parser("validate", help="validate a YAML configuration file")
    p.add_argument("file")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("convert", help="convert a YAML file to JSON")
    p.add_argument("file")
    p.set_defaults(func=cmd_convert)

    p = sub.add_parser("inspect", help="list top-level keys and their types")
    p.add_argument("file")
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("serve", help="serve a YAML file as JSON over HTTP")
    p.add_argument("file")
    p.add_argument("--port", type=int, default=8000)
    p.set_defaults(func=cmd_serve)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
