import os
import shutil

# capture the path of the file to be parsed
file_to_be_parsed = "tut03/regtable_old.csv"
header_row = "rollno,register_sem,sub_no,sub_type\n"

def output_by_subject():
	root_dir = "tut03/output_by_subject"
	file = open(file_to_be_parsed)

	# ALWAYS create a new directory, if it already exists, DELETE it
	if(os.path.exists(root_dir)):
		shutil.rmtree(root_dir)
	os.mkdir(root_dir)

	# iterate over the contents of the file
	for i, line in enumerate(file.readlines()):
		if i == 0:
			continue
		lst = line.split(',') # split the contents of a `line` by comma, for ease of accessibility of its elements

		# output file name
		output_file = os.path.join(root_dir,  lst[3] + ".csv")

		# create outputfile if it doesn't exist, and dump the contents of first row in it, manually
		if not os.path.exists(output_file):
			with open(output_file, "w") as header_stream:
				header_stream.write(header_row)
		
		# create a new stream and write contents to the corresponding row(s) to the desired file
		stdout_stream = open(output_file, "a")
		row_contents = lst[0] + "," + lst[1] + "," + lst[3]+ "," + lst[8]
		stdout_stream.write(row_contents)
	stdout_stream.close()
	return

def output_individual_roll():
	file = open(file_to_be_parsed)
	root_dir = "tut03/output_individual_roll"

	# ALWAYS create a new directory, if it already exists, DELETE it
	if(os.path.exists(root_dir)):
		shutil.rmtree(root_dir)
	os.mkdir(root_dir)

	# iterate over the contents of the file
	for idx, line in enumerate(file.readlines()):
		if idx == 0:
			continue
		lst = line.split(',') # split the contents of a `line` by comma, for ease of accessibility of its elements

		# output file name
		output_file = os.path.join(root_dir, lst[0] + ".csv")

		# create outputfile if it doesn't exist, and dump the contents of first row in it, manually
		if not os.path.exists(output_file):
			with open(output_file, "w") as header_stream:
				header_stream.write(header_row)

		# create a new stream and write contents to the corresponding row(s) to the desired file
		stdout_stream = open(output_file, "a")
		row_contents = lst[0] + "," + lst[1] + "," + lst[3] + "," + lst[8]
		stdout_stream.write(row_contents)
	stdout_stream.close()
	return

output_by_subject()
output_individual_roll()