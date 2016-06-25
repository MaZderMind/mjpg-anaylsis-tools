#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys, argparse, logging, requests

# Gather our code in a main() function
def main(args):
  logging.info("readming mjpeg-stream from %s", args.url);
  req = requests.get(args.url, stream=True)
  logging.debug("received headers: %s", req.headers);


  ctype = req.headers["Content-Type"]
  if not ctype.startswith("multipart/x-mixed-replace"):
    logging.error("document content-type is %s, not 'multipart/x-mixed-replace'", ctype)
    return False;


  paramstrs = ctype.split(";")[1:]
  parampairs = [s.split("=", 1) for s in paramstrs]
  params = {k: v for k,v in parampairs}
  logging.debug("parsed content-type params: %s", params);

  if not "boundary" in params:
    logging.error("no boundary-param declared in the content-type %s", ctype)
    return False;

  boundary = params["boundary"]
  if len(boundary) < 16:
    logging.warning("boundary is a little shorts (only %u characters)", len(boundary))


  logging.info("boundary parsed: %s", boundary)
  logging.debug("start parsing stream")




# setup commandline tool
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description = "Measure fps and jitter of an MJPEG-Stream")

  parser.add_argument("url",
    help = "Thw http(s) url to read the mjpeg-stream from",
    metavar = "ARG")

  parser.add_argument("-v", "--verbose",
    help="increase output verbosity",
    action="store_true")

  args = parser.parse_args()


  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  # enter main program
  main(args)
