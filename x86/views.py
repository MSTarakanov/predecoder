from django.shortcuts import render

# Create your views here.

def index(request, example_id):
    commands = []
    counter = 1
    stream = []
    values = []
    formats = []
    stream_begin = ''

    if request.method == 'POST':
        if 'example' in request.POST:
            counter = 0
            example_id = int(request.POST['example'])
    example = example1
    if example_id == 2:
        example = example2

    for command_desc in example:
        stream.append(command_desc['byte'])
        commands.append(command_desc['command'])

    if counter > 0:
        stream_begin = ''.join(stream[:counter])
    stream_selected = stream[counter]
    stream_end = ''.join(stream[counter + 1:])

    commands_tail = commands[:counter]
    current_command = commands[counter]

    for desc in example1[counter]['description']:
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

example1 = [{'byte': 'byte1', 'description': [['opcode', '0x8B', '8 бит'], ['immediate', '0x000000', '32 бит']], 'command': 'MOV EAX, 0'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'}]

example2 = [{'byte': 'byte1', 'description': [['opcode', '0x8B', '8 бит'], ['immediate', '0x000000', '32 бит']], 'command': 'MOV EAX, 0'},
            {'byte': 'byte2', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'},
            {'byte': 'byte3', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'},
            {'byte': 'byte4', 'description': [['opcode', '0x2B', '8 бит'], ['immediate', '0x00032', '16 бит']], 'command': 'ROX 33, U'}]