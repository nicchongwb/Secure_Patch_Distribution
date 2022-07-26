import os, re, sys, subprocess
import argparse
import hashlib, json

# Global
mem_placeholder = 'MEMORY_ADDR'
st_size_placeholder = ''
file_size_placeholder = 'FILE_SIZE'
time_placeholder = 'DATE_TIME'

syscall_arr = []
file_hashes = []

# Regex
eval_pattern = re.compile(r"\s=\s.+")  # find \s=\s\w+
mem_pattern = re.compile(r"0x\w+")  # find all 0x...
syscall_pattern = re.compile(r"\w+\(.+\)")  # find all syscall
var_pattern = re.compile(r"\/\*\s\w+\s\w+\s\*\/")  # find all \* var...
st_size = re.compile(r"=\d+")  # find all st_size
file_size = re.compile(r"[0-9]\w+")  # find all file_size
time_pattern = re.compile(r"\/\*\s\d+\-.+")  # find all \* date time...


# class Node:
#     def __init__(self, left, right, value: str,contnet) -> None:
#         self.left: Node - left

class MerkelTreeHash(object):
    def __init__(self):
        pass

    def find_merkel_hash(self, file_hashes):
        blocks = []

        if not file_hashes:
            raise ValueError(
                'Missing required file hashes for computing merkel tree hash'
            )

        for m in sorted(file_hashes):
            blocks.append(m)

        list_len = len(blocks)

        while list_len % 2 != 0:
            blocks.extend(blocks[-1:])
            list_len = len(blocks)

        secondary = []
        for k in [blocks[x:x + 2] for x in range(0, len(blocks), 2)]:
            hasher = hashlib.sha256()
            hasher.update(k[0].encode("utf-8") + k[1].encode("utf-8"))
            secondary.append(hasher.hexdigest())

        if len(secondary) == 1:
            return secondary[0]
        else:
            return self.find_merkel_hash(secondary)

def main():
    parser = argparse.ArgumentParser(description='Syscall Extractor')

    parser.add_argument('-f', '--file', required=True, help='file path of patch')
    args = parser.parse_args()

    # Set variables
    if_path = args.file  # input file path
    of_path = args.file + '_strace.txt'  # output file path

    # Check if file exist
    if not os.path.exists(if_path):
        sys.exit('[!] Error: %s not found!' % if_path)

    command = 'strace -v -s 100 ./%s 2> %s' % (if_path, of_path)
    print('[+] Executing %s ...' % command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    # strace output file stream
    strace_ifs = open(of_path, "r")  # strace input filestream
    lines = strace_ifs.readlines()
    n = 1
    for line in lines:
        # Remove all the < = ...> in syscall() = ...
        mod_line = re.sub(eval_pattern, '', line.strip())
        mod_line = re.sub(mem_pattern, mem_placeholder, mod_line.rstrip())
        mod_line = re.sub(var_pattern, '', mod_line.rstrip())
        mod_line = re.sub(st_size, st_size_placeholder, mod_line.rstrip())
        mod_line = re.sub(time_pattern, time_placeholder, mod_line.rstrip())

        #Look for munmap and mmap in syscall
        #Replace file size with placeholder in munmap and mmap syscall
        munmap = re.findall("munmap", line)
        mmap = re.findall("mmap", line)
        if munmap:
            mod_line = re.sub(file_size, file_size_placeholder, mod_line.rstrip())

        if mmap:
            mod_line = re.sub(file_size, file_size_placeholder, mod_line.rstrip())

        #Remove syscall1
        execve = re.findall("execve", line)

        for i in execve:
            mod_line = re.sub(i, st_size_placeholder, mod_line.rstrip())

        if re.match(syscall_pattern, mod_line):
            # hash syscalls
            hash = hashlib.sha256(mod_line.encode())
            syscall_id = 'syscall_%s' % n
            syscall_dict = {syscall_id: {'sha256': hash.hexdigest(), 'syscall': mod_line}}
            syscall_arr.append(syscall_dict)
            n += 1
    strace_ifs.close()

    # Convert syscall_arr to JSON
    ojf_path = args.file + '_od.json'  # output json file path
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
            # print(js[key]['sha256'])
            file_hashes.append(js[key]['sha256'])
    od_json.close()

    #print('Finding the merkle tree hash of {0} hashes'.format(len(file_hashes)))
    cls = MerkelTreeHash()
    mk = cls.find_merkel_hash(file_hashes)
    root = 'The merkle tree root hash of the {0} syscall hashes '.format(len(file_hashes)) + 'is : {0}'.format(mk)
    #print(root)

    #Append final root hash to Json
    command2 = 'echo : %s >> %s' % (root, ojf_path)
    # print('[+] Executing %s ...' % command2)
    process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, shell=True)

    #Vendor Open Declaration
    vod = 'vendor_' + args.file + '_od.json'  # output json file path

    #Omit ./ from path
    vod_path = vod.replace('./', '')

    #Find diff between Vendor OD and Verifier generated OD
    command3 = 'diff %s %s' % (vod_path, ojf_path)
    process3 = subprocess.Popen(command3, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process3.communicate()
    if stdout:
        sys.stdout.write(stdout.decode(sys.stdout.encoding))
    else:
        print("Merkle root hash and open declaration matched")

if __name__ == '__main__':
    main()

