from django.shortcuts import render
from .models import IntelDescription
# Create your views here.

def get_users_counter(request):
    counter = 0
    try:
        counter = IntelDescription.objects.get(user=request.user).counter
    except:
        print('no counter for this user')
    return counter

def set_users_counter(new_value, request):
    try:
        desc = IntelDescription.objects.get(user=request.user)
        desc.counter = new_value
        desc.save()
    except:
        print('no counter for this user')

def get_user_example_id(request):
    example_id = 1
    try:
        example_id = IntelDescription.objects.get(user=request.user).example_id
    except:
        print('no example_id for this user')
    return example_id

def set_user_example_id(new_value, request):
    try:
        desc = IntelDescription.objects.get(user=request.user)
        desc.example_id = new_value
        desc.save()
    except:
        print('no example_id for this user')


def index(request, example_id):
    commands = []
    counter = 1
    stream = []
    values = []
    formats = []
    stream_begin = ''

    counter = get_users_counter(request)
    example_id = get_user_example_id(request)

    if request.method == 'POST':
        print(request.POST)
        if 'example' in request.POST:
            new_example_id = int(request.POST['example'])
            set_users_counter(0, request)
            counter = 0
            set_user_example_id(new_example_id, request)
            example_id = get_user_example_id(request)


    try:
        example = examples[example_id - 1]
    except:
        example = examples[0]

    for command_desc in example:
        stream.append(command_desc['byte'])
        commands.append(command_desc['command'])

    counter_max = len(stream)
    if request.method == 'POST':
        print(counter, counter_max)
        if 'next' in request.POST and counter + 1 < counter_max:
            set_users_counter(counter+1, request)
            counter = get_users_counter(request)
        elif 'back' in request.POST and counter > 0:
            set_users_counter(counter - 1, request)
            counter = get_users_counter(request)
    if counter > 0:
        stream_begin = ''.join(stream[:counter])
    stream_selected = stream[counter]
    stream_end = ''.join(stream[counter + 1:])

    commands_tail = commands[:counter]
    current_command = commands[counter]

    for desc in example[counter]['description']:
        formats.append(desc[0])
        values.append(desc[1])


    context = {
        'commands_tail': commands_tail,
        'current_command': current_command,
        'stream': stream,
        'formats': formats,
        'values': values,
        'stream_begin': stream_begin,
        'stream_selected': stream_selected,
        'stream_end': stream_end,
    }
    return render(request, 'x86/x86_main.html', context)

examples = [
            [{'byte': '66A100403000', 'description': [['Prefix', '0x66', '8 бит'], ['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00403000', '32 бит']], 'command': 'MOV AX, U'},
            {'byte': '66F72D004030A1', 'description': [['Prefix', '0x66', '8 бит'],['Opcode', '0x89', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'IMUL V'},
            {'byte': '6689C3', 'description': [['Prefix', '0x66', '8 бит'],['Opcode', '0x89', '8 бит'], ['Mod R/M', '0xC3', '16 бит']], 'command': 'MOV BX, AX'},
            {'byte': '66A10040303F', 'description': [['Prefix', '0x66', '8 бит'], ['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00603000', '32 бит']], 'command': 'MOV AX, Z'},
            {'byte': '6629D8', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'SUB AX, BX'},
            {'byte': '66F73D0040307D', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'IDIV W'},
            {'byte': '66030500403AFF', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ADD AX, Y'},
            {'byte': '66A300402000', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'MOV X, AX'}],

    [{'byte': '33F6', 'description': [['Opcode', '0x33', '8 бит'], ['Mod R/M', '0xF6', '8 бит']],
      'command': 'XOR ESI, ESI'},
     {'byte': 'A100403000', 'description': [['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00403000', '32 бит']],
      'command': 'MOV EAX, [0x00403000]'},
     {'byte': '8B1D00403000', 'description': [['Opcode', '0x8B', '8 бит'], ['Mod R/M', '0x1D', '8 бит'],
                                              ['Displacement', '0x00403000', '32 бит']],
      'command': 'MOV EBX, [0x00403000]'},
     {'byte': 'B900403000', 'description': [['Opcode', '0xB9', '8 бит'], ['Immediate', '0x00000003', '32 бит']],
      'command': 'MOV ECX, 3'},
     {'byte': 'EB58', 'description': [['Opcode', '0xEB', '8 бит'], ['Displacement', '0x58', '8 бит']],
      'command': 'JMP [0x58]'},
     {'byte': '3B8600403000', 'description': [['Opcode', '0x3B', '8 бит'], ['Mod R/M', '0x86', '8 бит'],
                                              ['Displacement', '0x00403000', '32 бит']],
      'command': 'CMP EAX, [0x00403000]'},
     {'byte': '741C', 'description': [['Opcode', '0x74', '8 бит'], ['Displacement', '0x1C', '8 бит']],
      'command': 'JE [0x1C]'},
     {'byte': '3B8600403000', 'description': [['Opcode', '0x3B', '8 бит'], ['Mod R/M', '0x86', '8 бит'],
                                              ['Displacement', '0x00403000', '32 бит']],
      'command': 'CMP EAX, [0x00403000]'},
     {'byte': '7C24', 'description': [['Opcode', '0x7C', '8 бит'], ['Displacement', '0x24', '8 бит']],
      'command': 'JL [0x24]'},
     {'byte': 'EB00', 'description': [['Opcode', '0xEB', '8 бит'], ['Displacement', '0x00', '8 бит']],
      'command': 'JMP [0x00]'},
     {'byte': '3B9E00403000', 'description': [['Opcode', '0x3B', '8 бит'], ['Mod R/M', '0x9E', '8 бит'],
                                              ['Displacement', '0x00403000', '32 бит']],
      'command': 'CMP EBX, [0x00403000]'},
     {'byte': '7412', 'description': [['Opcode', '0x74', '8 бит'], ['Displacement', '0x12', '8 бит']],
      'command': 'JE [0x12]'},
     {'byte': '7412', 'description': [['Opcode', '0x74', '8 бит'], ['Displacement', '0x12', '8 бит']],
      'command': 'JE [0x12]'}],

[{'byte': 'D90500402000', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b1', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b000', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00402000', '32 бит']], 'command': 'FLD [0x00402000]'},
            {'byte': 'D80D00402000', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b0', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b001', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00402000', '32 бит']], 'command': 'FMUL [0x00402000]'},
            {'byte': 'D90500402004', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b1', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b000', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00402004', '32 бит']], 'command': 'FLD [0x00402004]'},
            {'byte': 'D80D00402004', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b0', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b001', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00402004', '32 бит']], 'command': 'FMUL [0x00402004]'},
            {'byte': 'DEC1', 'description': [['Opcode', '0xDE', '8 бит'], ['Mod R/M', '0xC1', '8 бит']], 'command': 'FADDP ST(1), ST'},
            {'byte': 'D9FA', 'description': [['Opcode', '0xD9', '8 бит'], ['Mod R/M', '0xFA', '8 бит']], 'command': 'FSQRT ST'},
            {'byte': 'DB3D00402008', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b01', '2 бита'], ['Opcode A', '0b1', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b111', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00403010', '32 бит']], 'command': 'FSTP [0x00402008]'}],

[{'byte': 'D90500403008', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b1', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b000', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00402000', '32 бит']], 'command': 'FLD [0x00403008]'},
            {'byte': 'D9FE', 'description': [['Opcode', '0xD9', '8 бит'], ['Mod R/M', '0xFE', '8 бит']], 'command': 'FSIN ST'},
            {'byte': 'D80D00403000', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b0', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b001', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00403000', '32 бит']], 'command': 'FMUL [0x00403000]'},
            {'byte': 'D80D00403004', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b0', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b001', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00403000', '32 бит']], 'command': 'FMUL [0x00403004]'},
            {'byte': 'D8350040300C', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b00', '2 бита'], ['Opcode A', '0b0', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b110', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x0040300C', '32 бит']], 'command': 'FDIV [0x0040300C]'},
            {'byte': 'DB3D00403010', 'description': [['Special code', '0b11011', '5 бит'], ['MF', '0b01', '2 бита'], ['Opcode A', '0b1', '1 бит'], ['Mod', '0b00', '2 бита'], ['Opcode B', '0b111', '3 бита'], ['R/M', '0b101', '3 бита'], ['Displacement', '0x00403010', '32 бит']], 'command': 'FSTP [0x00403010]'}],


]