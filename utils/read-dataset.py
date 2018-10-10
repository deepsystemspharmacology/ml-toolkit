#
# file: read-dataset.py
# 
# This file takes in a path to training data that contains named folders for each class
# with text files of points/matrices within each file
#

import numpy as np
import os
import random
import sys

def read_2d_matrix(file):
	# read in 2d matrix
	sample = np.loadtxt(file)

	# get rid of first 2 columns bc irrelevant to distance matrix
	return sample[:, 2:]	

def read_point_data(file):
	sample = np.loadtxt(file)

	return sample[:,2:]


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("usage: python create-sid.py [dir] [type] [out_name]")
		print("dir: directory to data")
		print("type: dist or point -- distance matrix or point data")
		print("out_name: file name to save the output to")
		sys.exit(1)


	INPUT_DIR = sys.argv[1]
	TYPE = sys.argv[2]

	if TYPE is not 'dist' or TYPE is not 'point':
		print("incorrect type parameter")

	OUTPUT_NAME = sys.argv[3]

	# get list of all subdirectories
	dirs = [d for d in os.listdir(INPUT_DIR) if os.path.isdir("%s/%s" % (INPUT_DIR, d))]
	dirs = ["%s/training-data" % (d) for d in dirs]

	# get list of all classes
	classes = [d.split("-")[0] for d in dirs]
	classes = list(set(classes))

	samples = []
	labels = []

	for i in range(len(classes)):
		print(classes[i])

		# get list of all files in class
		class_dirs = ["%s/%s" % (INPUT_DIR, d) for d in dirs if d.split("-")[0] == classes[i]]
		files = sum([["%s/%s" % (d, f) for f in os.listdir(d)] for d in class_dirs], [])

		for f in files:
			if TYPE is dist:
				sample = read_2d_matrix(f)
			elif TYPE is point:
				sample = read_point_data(f)

			# create one hot labels
			label = np.zeros(len(classes))
			label[i] = 1

			# add sample and label to list
			samples.append(sample)
			labels.append(label)

	# convert samples and labels to numpy format
	np_samples = np.asarray(samples)
	np_labels = np.asarray(labels)

	# save output files
	np.save(OUTPUT_NAME + '_samples.npy', np_samples)
	np.save(OUTPUT_NAME + '_labels.npy', np_labels)
