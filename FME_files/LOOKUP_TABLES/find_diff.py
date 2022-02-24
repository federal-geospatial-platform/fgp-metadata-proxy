import glob
import os
import difflib

P_T_ABBR = ["AB", "BC", "MB", "NB", "NS", "ON", "PEI", "SK", "QC", "YT"]

def compare_file(norm_file_a, norm_file_b):
    """Read the files and compare the content"""

    with open(norm_file_a, 'r') as f:
        file_a_lines = f.readlines()

    with open(norm_file_b, 'r') as f:
        file_b_lines = f.readlines()

    # Compare content
    diff_lines = difflib.unified_diff(file_a_lines, file_b_lines, lineterm='')

    diff_lines = list(diff_lines)

    return diff_lines



def normalize_file(file):
    """Normalize the file name by removing the prefixe or suffixe of the file name
    """

    base_name = os.path.basename(file)
    splits = base_name.split(".")
    file_name = splits[0]
    ext_name = splits[1]


    # Try to remove the suffix or prefix
    for p_t_abbr in P_T_ABBR:
        suffix = "_" + p_t_abbr
        prefix = p_t_abbr + "_"
        if file_name.endswith(suffix):
            file_name = file_name.rstrip(suffix)
            break
        if file_name.startswith(prefix):
            file_name = file_name.lstrip(prefix)
            break

    return file_name

# Initialize counter
different = 0
identical = 0

# Create a list of all the *.yaml files
files = glob.glob(r'.\*\*.yaml')

file_out = open("result_diff.txt", "w", newline=None)

# Loop over each file in order to compare them file by file
nbr_files = len(files)


for i in range(nbr_files):
    file_a = files[i]
    norm_file_a = normalize_file(file_a)
    for j in range(i+1, nbr_files):
        file_b = files[j]
        norm_file_b = normalize_file(file_b)

        if norm_file_a == norm_file_b:
            diff_lines = compare_file(file_a, file_b)
            if diff_lines:
                txt = ""
                print(txt)
                file_out.write(txt + "\n")
                txt = "*** Files are different: {0} versus {1}".format(file_a, file_b)
                print(txt)
                file_out.write(txt + "\n")
                different += 1
                for diff_line in diff_lines:
                    print(diff_line)
                    file_out.write(diff_line)
            else:
                txt = "... Files are identical: {0} versus {1}".format(file_a, file_b)
                print(txt)
                file_out.write(txt + "\n")
                identical += 1

txt1 = " "
txt2 = "Statistics"
txt3 = "----------"
txt4 = "File identical: {0}".format(identical)
txt5 = "File different: {0}".format(different)
print(txt1)
print(txt2)
print(txt3)
print(txt4)
print(txt5)
file_out.write(txt1 + "\n")
file_out.write(txt1 + "\n")
file_out.write(txt2 + "\n")
file_out.write(txt3 + "\n")
file_out.write(txt4 + "\n")
file_out.write(txt5 + "\n")

file_out.close()
