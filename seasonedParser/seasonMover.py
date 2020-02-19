#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-11 19:16:23
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-08-13 12:12:05

import fire, re, os
from pprint import pprint

class seasonMover(object):
	''' Moving multiple files to multiple folders with 
	identifer '''
	workingDir = os.getcwd()
	mediaExt = ['mkv', 'mp4']
	subExt = ['srt']

	def create(self, name, interval):
		pass

	def move(self, fileSyntax, folderName):
		episodeRange = self.findInterval(fileSyntax)
		episodeList = self.getFiles()
			
		self.motherMover(fileSyntax, folderName, episodeRange)


	def getFiles(self):
		epDir = os.path.join(self.workingDir)
		dirContent = os.listDir(epDir)
		fileList = sorted(dirContent)
		return fileList

	def getEpisodeNumber(self):
		m = re.search('[eE][0-9]{1,2}', self.parent)
		if m:
			return re.sub('[eE]', '', m.group(0))

	# def findInterval(self, item):
	# 	if (re.search(r'\((.*)\)', item) is None):
	# 		raise ValueError('Need to declare an identifier e.g. (1..3) in: \n\t' + item)

	# 	start = int(re.search('\((\d+)\.\.', item).group(1))
	# 	end = int(re.search('\.\.(\d+)\)', item).group(1))

	# 	return list(range(start, end+1))

	def removeUploadSign(self, file):
		match = re.search('-[a-zA-Z\[\]\-]*.[a-z]{3}', file)
		if match:
			uploader = match.group(0)[:-4]
			return re.sub(uploader, '', file)

		return file

	def motherMover(self, fileSyntax, folderName, episodeRange):
		# Call for sub of fileList
		# TODO check if range is same as folderContent
		# print(fileSyntax, folderName, episodeRange)
		mediaFiles = []
		subtitleFiles = []
		seasonDirectory = sorted(os.listdir(os.path.join(self.workingDir)))

		for file in seasonDirectory:
			if file[-3:] in self.mediaExt:
				mediaFiles.append(file)
			elif file[-3:] in self.subExt:
				subtitleFiles.append(file)

		if (len(mediaFiles) is not len(episodeRange)):
			raise ValueError('Range defined does not match directory file content')

		for epMedia, epNum in zip(mediaFiles, episodeRange):
			leadingZeroNumber = "%02d" % epNum
			fileName = re.sub(r'\((.*)\)', leadingZeroNumber, fileSyntax)
			oldPath = os.path.join(self.workingDir, epMedia)
			newFolder = os.path.join(self.workingDir, folderName + leadingZeroNumber)
			newPath = os.path.join(newFolder, self.removeUploadSign(fileName))

			# os.makedirs(newFolder)
			# os.rename(oldPath, newPath)
			print(oldPath + ' --> ' + newPath)


if __name__ == '__main__':
	fire.Fire(seasonMover)
	