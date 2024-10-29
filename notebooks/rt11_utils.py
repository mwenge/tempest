import os
import math

EOS_MARKER = 0x0800
EMPTY = 0x0200
TENTATIVE = 0x0100

CHARS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ$.*0123456789"

def radix50_decode(v):
    if v > 63999:
        raise Exception("Invalid Value")
    c1 = math.floor(v/(40**2))
    v2 = v%(40**2)
    c2 = math.floor(v2/40)
    c3 = v2%40
    return CHARS[c1]+CHARS[c2]+CHARS[c3]

def radix50_encode(chars):
    if len(chars) != 3:
        raise Exception("Must be 3 characters")
    result = ((CHARS.index(chars[0]) * (40**2)) + 
              (CHARS.index(chars[1]) * (40)) + 
              CHARS.index(chars[2]))
    return result

def extract_files_from_disk(disk_file, destination_folder):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    rk1 = open(disk_file,'rb')
    header = rk1.read(0xc00)
    no_segments = int.from_bytes(rk1.read(2), "little")
    segment_no = int.from_bytes(rk1.read(2), "little")
    segment_highest = int.from_bytes(rk1.read(2), "little")
    extra_bytes = int.from_bytes(rk1.read(2), "little")
    start_block = int.from_bytes(rk1.read(2), "little") # blocks are 512 bytes

    segment_header = [
        no_segments,
        segment_no,
        segment_highest,
        extra_bytes,
        start_block
    ]
    entries = []
    while True:
        status_word = int.from_bytes(rk1.read(2), "little")
        if not status_word or status_word == EOS_MARKER:
            break

        first_three_chars = radix50_decode(int.from_bytes(rk1.read(2), "little"))
        second_three_chars = radix50_decode(int.from_bytes(rk1.read(2), "little"))
        third_three_chars = radix50_decode(int.from_bytes(rk1.read(2), "little"))
        no_octal_blocks = int.from_bytes(rk1.read(2), "little")
        reserved = int.from_bytes(rk1.read(2), "little")
        file_date = int.from_bytes(rk1.read(2), "little")

        entries += [[
            status_word,
            first_three_chars,
            second_three_chars,
            third_three_chars,
            no_octal_blocks,
            reserved,
            file_date
        ]]
    #print("segment header",segment_header)

    rk1.seek(start_block * 512)
    for entry in entries:
        #print("entry", entry)
        file_name = ''.join(entry[1:3])+'.'+entry[3]
        file_length = entry[4] * 512
        file_data = rk1.read(file_length)
        if entry[0] == EMPTY or entry[0] == TENTATIVE:
            file_name += "_UNUSED"

        #print(file_name,file_data[:10],hex(rk1.tell()))
        open(f"{destination_folder}/{file_name}",'wb').write(file_data)

word = lambda x: (x).to_bytes(2,"little")
read_word = lambda x: int.from_bytes(x,"little")

def parse_lda_file(filename):
    BLOCK_HEADER = b'\x01\x00'
    LDA_END = 0x0000
    
    al = open(filename,'rb')
    blocks = []
    while True:
        sentinel = al.read(2)
        if sentinel != BLOCK_HEADER:
            raise Exception("Block Header Expected But Got: ", sentinel)

        len_data = read_word(al.read(2)) - 6
        # Have we reached the end of our blocks?
        if len_data == LDA_END:
            break

        addr = read_word(al.read(2))
        data = al.read(len_data)
        checksum = al.read(1)
        blocks += [(hex(addr),addr,len(data),data)]
        
    # Use the addresses given in our datablocks to populate
    # a bytearray of all of the ROM data.
    output_bytes = bytearray(b'\x00' * 0xFFFF)
    for _,addr,len_data,data in blocks:
        output_bytes[addr:addr+len_data] = data

    return output_bytes

word = lambda x: (x).to_bytes(2,"little")

# See `AA-PD6PA-TC_RT-11_Volume_and_File_Formats_Manual_Aug91.pdf` in `../materials`
def create_disk_from_files(src_folder, disk_name, suffices=[]):
    BLOCK_LENGTH = 512
    FILES_START = 0x4c00

    # Read in each source file from the git repo we cloned
    files_to_write = []
    for file_name in os.listdir(src_folder):
        if suffices and file_name[-3:] not in suffices:
            continue
        data = open(src_folder+'/'+file_name,'rb').read().strip().strip(b'\x00')
        files_to_write += [(file_name,data,len(data))]

    # Copy in the home block header from another disk image
    header = b'\xa0\x007\x08$\x00\r\x00\x00\x00\x00\n?BOOT-F-No boot on volume\r\n\n\x80\x00\xdf\x8bt\xff\xfd\x80\x1f\x94v\xff\xfa\x80\xff\x01'
    header += (b'\x00' * 922)
    header += b'\x01\x00\x06\x00\xa9\x8eRT11A                   DECRT11A    '
    header += (b'\x00' * 2052)

    # Header for the directory entry
    dir_entry = word(16) + word(0) + word(1) + word(0) + word(38)
    # The file data for the main part of the disk
    file_data = b''

    # Write a directory entry for each file and append its zero-padded data
    # to file_data for writing later
    for (filename,data,file_len) in files_to_write:
        #filetype
        dir_entry += word(0x0400)

        #filename
        filename = filename.split('.')
        trio1 = filename[0][:3].ljust(3)
        trio2 = filename[0][3:].ljust(3)
        trio3 = filename[1].ljust(3)
        dir_entry += word(radix50_encode(trio1))
        dir_entry += word(radix50_encode(trio2))
        dir_entry += word(radix50_encode(trio3))

        # No of blocks used by file
        blocks = math.floor(file_len/BLOCK_LENGTH) + 1
        dir_entry += word(blocks)

        #reserved
        dir_entry += word(0)
        #filedate
        dir_entry += word(0)

        # add the file data
        padding = b'\x00' * ((blocks*BLOCK_LENGTH) - file_len)
        file_data += data + padding

    # Create an empty entry so we have some free space to write 
    # the object files to when we assemble and link.
    #filetype
    dir_entry += word(0x0200)
    dir_entry += word(radix50_encode("EM "))
    dir_entry += word(radix50_encode("PTY"))
    dir_entry += word(radix50_encode("FIL"))
    # number of blocks
    dir_entry += word(5200)
    #reserved
    dir_entry += word(0)
    #filedate
    dir_entry += word(0)

    # Add the end segment to the end of the directory structure
    dir_entry += word(0x0800)

    # Padding for the directory block
    total_so_far = len(header + dir_entry)
    dir_entry_padding = b'\x00' * (FILES_START - total_so_far)

    # Padding for the main block
    main_data = header + dir_entry + dir_entry_padding + file_data
    #main_padding = b'\x00' * (0x261200 - len(main_data))

    # Write everything to our image file
    open(disk_name,'wb').write(main_data)

    #!xxd tempest_original.rk05