import os, re, sys, subprocess
import argparse
import hashlib, json

# Global
mem_placeholder = 'MEMORY_ADDR' 
syscall_arr = []

# Regex
eval_pattern = re.compile(r"\s=\s.+") # find \s=\s\w+
mem_pattern = re.compile(r"0x\w+") # find all 0x...
syscall_pattern = re.compile(r"\w+\(.+\)") # find all syscall

class Node:
    def __init__(self, left, right, value: str,contnet) -> None:
        self.left: Node - left

def main():
    parser = argparse.ArgumentParser(description='Syscall Extractor')

    parser.add_argument('-f', '--file', required=True, help='file path of patch')
    args = parser.parse_args()

    # Set variables
    if_path = args.file # input file path
    of_path = args.file + '_strace.txt' # output file path

    # Check if file exist
    if not os.path.exists(if_path):
        sys.exit('[!] Error: %s not found!' % if_path)

    command = 'strace ./%s 2> %s' % (if_path, of_path)
    print('[+] Executing %s ...' % command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    # strace output file stream
    strace_ifs = open(of_path, "r") # strace input filestream
    lines = strace_ifs.readlines()
    n = 1
    for line in lines:
        # Remove all the < = ...> in syscall() = ...
        mod_line = re.sub(eval_pattern, '', line.strip())
        mod_line = re.sub(mem_pattern, mem_placeholder, mod_line.rstrip())
        if re.match(syscall_pattern, mod_line):
            # hash syscall
            hash = hashlib.sha256(mod_line.encode())
            syscall_id = 'syscall_%s' % n
            syscall_dict = {syscall_id:{'sha256':hash.hexdigest(), 'syscall':mod_line}}
            syscall_arr.append(syscall_dict)
            n += 1
    strace_ifs.close()

    # Convert syscall_arr to JSON
    ojf_path = args.file + '_od.json' # output json file path
    with open(ojf_path, "w") as od_json:
        for syscall in syscall_arr:
            json.dump(syscall, od_json)
            od_json.write('\n')
    od_json.close()

    # Merkle Tree Generation
    with open(ojf_path, 'r') as od_json:
        for line in od_json:
            js = json.loads(line)
            key = list(js.keys())[0]
            print(js[key]['sha256'])
    od_json.close()

if __name__ == '__main__':
    main()
