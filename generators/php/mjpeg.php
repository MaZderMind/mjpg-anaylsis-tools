<?php

$fps = 5;
$boundary = "3cd47a181ec2129228c1e8784cd97e7a2473a5de";
header("Content-Type: multipart/x-mixed-replace;boundary=$boundary;lala=baba");
header("Cache-Control: no-cache");
header("Cache-Control: private");

$which = true;

$a = file_get_contents('a.jpg');
$asz = strlen($a);

$b = file_get_contents('b.jpg');
$bsz = strlen($b);


while(true)
{
	print("--$boundary\n");
	print("Content-Type: image/jpeg\n");
	print("Content-Length: ".($which ? $asz : $bsz)."\n\n");
	print($which ? $a : $b);
	flush();

	$which = !$which;
	usleep(1/$fps * 1000000);
}
