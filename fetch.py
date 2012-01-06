#! /usr/bin/env python2

import os
import mimetypes
from functools import partial
import eyeD3

noextract = False

trysplit = lambda s, *args:None if s == None else s.split(*args)

def ismime(filename,mmtype):
	mtype = mimetypes.guess_type(filename)[0]
	if mtype == None:
		return False
	return mtype.split('/')[0] == mmtype

isaudio = partial(ismime, mmtype='audio')
isimage = partial(ismime, mmtype='image')

def mainfunc(pat):
	tag = eyeD3.Tag()
	for dpath, dnames, filenames in os.walk(pat):
		if not any(isaudio(filename) for filename in filenames):
			continue
		if any(isimage(filename) for filename in filenames):
			continue
		if noextract:
			print dpath
			continue
			
		madefile = False
		for f in (os.path.join(dpath,f) for f in filenames if isaudio(os.path.join(dpath,f))):
			tag.link(f)
			imgs = tag.getImages()
			if imgs == None or len(imgs) <=0:
				continue
			imgs = imgs[0]
			imgs.writeFile(path=dpath,name="folder."+imgs.mimeType.split("/")[1].lower())
			madefile = True
			break
		if not madefile:
			print dpath

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="checks if an image is in a directory with an audio format")
	parser.add_argument('paths', metavar='path', type=unicode, nargs='*',
					   help='paths', default=['.'])
	parser.add_argument('--noextract', dest='noextract', default=False, action='store_const', const=True)
					   
					   
	args = parser.parse_args()
	noextract = args.noextract
	for pat in args.paths:
		mainfunc(pat)
	