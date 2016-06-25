#!/bin/sh
echo 'Content-Type: multipart/x-mixed-replace;boundary=3cd47a181ec2129228c1e8784cd97e7a2473a5de';
echo 'Cache-Control: no-cache';
echo 'Cache-Control: private';
echo ''

gst-launch-1.0 videotestsrc !\
        video/x-raw,width=1920,height=1080,framerate=25/1 !\
        jpegenc !\
        queue !\
        multipartmux boundary=3cd47a181ec2129228c1e8784cd97e7a2473a5de !\
        queue !\
        fdsink sync=false
