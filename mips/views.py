from django.shortcuts import render, redirect
from .forms import BytesField

# Create your views here.




def index(request):
    error_title = "None"
    form = BytesField()
    global stream

    if request.method == 'POST':
        print(request.POST)
        if 'next' in request.POST:
            form = BytesField(request.POST)
            if form.is_valid():
                bytes_string = form.cleaned_data['text']
                error_title = error_for_bytes_string(bytes_string)
                if error_title == "None":
                    # render process page
                    print(request.POST)
                    stream = bytes_string
                    global counter
                    counter = 0
                    return redirect('process/')
                    #return render(request, 'mips/mips_process.html')
        elif 'example' in request.POST:
            example_id = request.POST['example'][0]
            if example_id == '1':
                form = BytesField(initial={'text': 'a1090000210800022129ffff0129001808100005'})
            elif example_id == '2':
                form = BytesField(initial={'text': 'asrfs'})
    return render(request, 'mips/mips_main.html', {'error_title': error_title, 'form': form, 'stream': stream})


def error_for_bytes_string(string):
    if len(string) % 4 != 0:
        return "Все инструкции MIPS должны занимать ровно по четыре байта!"
    return "None"


counter = 0
stream = ""


def process(request):
    global stream
    stream_parts = [''.join(i) for i in grouper(stream, 8)]
    counter_max = len(stream_parts) - 1
    global counter
    if request.method == 'POST':
        if 'back' in request.POST:
            if counter > 0:
                counter -= 1
            else:
                return redirect('mips_main')
        elif 'next' in request.POST and counter < counter_max:
            counter += 1
    stream_begin = ''
    bytes = []
    bits = []
    commands = []
    operation_type = "I-Type"

    print(request.POST)

    if counter > 0:
        stream_begin = ''.join(stream_parts[:counter])
    stream_selected = stream_parts[counter]
    stream_end = ''.join(stream_parts[counter+1:])

    bytes = [stream_selected[0:2], stream_selected[2:4], stream_selected[4:6], stream_selected[6:8]]
    four_bytes = ''.join(bytes)

    bits = str("{0:032b}".format(int(stream_selected, 16)))

    commands = stream_to_commands(stream_parts)

    if bits[0:6] == "000000":
        operation_type = "R-Type"
        rs = registers[bits[6:11]]
        rt = registers[bits[11:16]]
        rd = registers[bits[16:21]]
        funct = functions[bits[26:32]]
        # commands.append(funct + ' ' + rs + ' ' + rt)
    elif bytes[0] == "08":
        operation_type = "J-Type"
        op = opcodes[bits[0:6]]
        addr = hex(int(bits[6:32], 2))
        # commands.append(op + ' ' + addr)
    else:
        operation_type = "I-Type"
        op = opcodes[bits[0:6]]
        rs = registers[bits[6:11]]
        rt = registers[bits[11:16]]
        immm = hex(int(bits[16:32], 2))
        # commands.append(op + ' ' + rs + ' ' + rt + ' ' + immm)

    commands_chain = ' -> '.join(commands[0:counter])
    if counter != 0:
        commands_chain += ' -> '
    command_selected = commands[counter]


    context = {
        'stream': stream,
        'stream_begin': stream_begin,
        'stream_selected': stream_selected,
        'stream_end': stream_end,
        'commands': commands,
        'commands_chain': commands_chain,
        'operation_type': operation_type,
        'bits': bits,
        'bytes': bytes,
        'four_bytes': four_bytes,
        'command_selected': command_selected,
    }
    return render(request, 'mips/mips_process.html', context)


def stream_to_commands(stream_parts):
    commands = []
    for part in stream_parts:
        bits = str("{0:032b}".format(int(part, 16)))
        bytes = [part[0:2], part[2:4], part[4:6], part[6:8]]
        if bits[0:6] == "000000":
            operation_type = "R-Type"
            rs = registers[bits[6:11]]
            rt = registers[bits[11:16]]
            rd = registers[bits[16:21]]
            funct = functions[bits[26:32]]
            commands.append(funct + ' ' + rs + ' ' + rt)
        elif bytes[0] == "08":
            operation_type = "J-Type"
            op = opcodes[bits[0:6]]
            addr = hex(int(bits[6:32], 2))
            commands.append(op + ' ' + addr)
        else:
            operation_type = "I-Type"
            op = opcodes[bits[0:6]]
            rs = registers[bits[6:11]]
            rt = registers[bits[11:16]]
            immm = hex(int(bits[16:32], 2))
            commands.append(op + ' ' + rs + ' ' + rt + ' ' + immm)

    return commands

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)

registers = {
    '00000': '$zero',
    '00001': '$at',
    '00010': '$v0',
    '00011': '$v1',
    '00100': '$a0',
    '00101': '$a1',
    '00110': '$a2',
    '00111': '$a3',
    '01000': '$t0',
    '01001': '$t1',
    '01010': '$t2',
    '01011': '$t3',
    '01100': '$t4',
    '01101': '$t5',
    '01110': '$t6',
    '01111': '$t7',
    '10000': '$s0',
    '10001': '$s1',
    '10010': '$s2',
    '10011': '$s3',
    '10100': '$s4',
    '10101': '$s5',
    '10110': '$s6',
    '10111': '$s7',
    '11000': '$t8',
    '11001': '$t9',
    '11010': '$k0',
    '11011': '$k1',
    '11100': '$gp',
    '11101': '$sp',
    '11110': '$fp',
    '11111': '$ra'
}

functions = {
    '000000': 'sll',
    '000010': 'srl',
    '000011': 'sra',
    '000100': 'sllv',
    '000110': 'srlv',
    '000111': 'srav',
    '001000': 'jr',
    '010000': 'mfhi',
    '010010': 'mflo',
    '011000': 'mult',
    '011010': 'div',
    '011011': 'divu',
    '100000': 'add',
    '100001': 'addu',
    '100010': 'sub',
    '100011': 'subu',
    '100100': 'and',
    '100101': 'or',
    '100110': 'xor',
    '100111': 'nor',
    '101010': 'slt'
}

opcodes = {
    '000010': 'j',
    '000011': 'jal',
    '000100': 'beq',
    '000101': 'bne',
    '001000': 'addi',
    '001001': 'addiu',
    '001010': 'slti',
    '001100': 'andi',
    '001101': 'ori',
    '001110': 'xori',
    '001111': 'lui',
    '100000': 'lb',
    '100001': 'lh',
    '100010': 'lw',
    '100011': 'ld',
    '100100': 'lbu',
    '100101': 'lhu',
    '101000': 'sb',
    '101001': 'sh',
    '101011': 'sw',
    '101010': 'test'
}
