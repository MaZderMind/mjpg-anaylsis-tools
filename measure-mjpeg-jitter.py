#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys, time, argparse, logging, requests

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


  # number of frames seen
  framecount = 0

  # sum of the sizes of frames seen
  framesize_sum = 0

  # sum of the duration in (mili?)seconds of frames seen
  framegap_sum = 0

  # durations in (mili?)seconds of frames seen
  framegaps = []


  # size of the last frame (working variable)
  framesize = 0

  # timsestamp of last frame seen (working variable)
  prevframe_stamp = time.time()


  while True:
    # 1. look for boundary-line
    logging.debug("looking for boundary-line")
    while True:
      line = req.raw.readline()
      if line.startswith("--" + boundary):
        logging.debug("found boundary-line after %u bytes", framesize)
        break

      # 1a. add over-read number of bytes to framesize
      framesize += len(line)

    # 2. record timing & size-information (if this is not the first boundary)
    if framesize > 0:
      framecount += 1
      framesize_sum += framesize

      framegap = time.time() - prevframe_stamp
      framegap_sum += framegap
      framegaps.append(framegap)

      # TODO: replace with better statistics function
      logging.info("frame of %u bytes after %fs", framesize, framegap)

      prevframe_stamp = time.time()
      framesize = 0

    # 3. read frame-headers
    frameheaders = {}
    while True:
      line = req.raw.readline().rstrip()
      if len(line) == 0:
        # empty line = enf of header
        break

      k, v = [s.strip().lower() for s in line.split(":", 1)]
      frameheaders[k] = v

    logging.debug("received frame-headers: %s", frameheaders);

    # 4. fail if no length or type is provided or type is wrong
    if not "content-type" in frameheaders:
      logging.warning("no frame content-type provided")

    if frameheaders["content-type"] != "image/jpeg":
      logging.warning("frame content-type is %s, not 'image/jpeg'", frameheaders["content-type"])

    if not "content-length" in frameheaders:
      logging.error("no frame content-length provided")
      return False

    length = int(frameheaders["content-length"])
    if length < 1:
      logging.warning("invalid frame content-length %d provided", length)
      continue

    # 4a. read that amount of bytes
    framedata = req.raw.read(length)

    # 4b. record read length as frame-size
    logging.debug("read %u bytes of frame-data", len(framedata))
    framesize += len(framedata)




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
