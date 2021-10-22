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

    if example_id == 2:
        example = example2
    else:
        example = example1

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

example1 = [{'byte': 'byte1', 'description': [['Prefix', '0x66', '8 бит'], ['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00403000', '32 бит']], 'command': 'MOV AX, U'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'IMUL V'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'MOV BX, AX'},
            {'byte': 'byte2', 'description': [['Prefix', '0x66', '8 бит'], ['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00603000', '32 бит']], 'command': 'MOV AX, Z'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'SUB AX, BX'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'IDIV W'},
            {'byte': 'byte2', 'description': [['Prefix', '0x66', '8 бит'], ['Opcode', '0xA1', '8 бит'], ['Displacement', '0x00503000', '32 бит']], 'command': 'ADD AX, Y'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'MOV X, AX'}]

example2 = [{'byte': 'byte1', 'description': [['opcode', '0x8B', '8 бит'], ['immediate', '0x000000', '32 бит'], ['opcode', '0x8B', '8 бит'], ['immediate', '0x000000', '32 бит'], ['immediate', '0x000000', '32 бит'], ['opcode', '0x8B', '8 бит']], 'command': 'MOV EAX, 0'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'},
            {'byte': 'byte3', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'},
            {'byte': 'byte4', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'}]