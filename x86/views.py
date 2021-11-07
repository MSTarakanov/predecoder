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
        example = examples[example_id - 1]['example']
        example_desc = examples[example_id - 1]['desc']
    except:
        example = examples[0]['example']
        example_desc = examples[0]['desc']

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
        'example_desc': example_desc,
        'examples_names': examples_names,
    }
    return render(request, 'x86/x86_main.html', context)

examples = [
    {'name': 'Вычисление выражения X = Y + (Z - U * V) / W',
     'desc': 'Так как мы используем регистры 32-битной разрядности, в составе каждой инструкции есть префикс х66, который указывает на это. Также, каждая переменная имеет свой адрес.' ,'example':
   [{'byte': '66A100403000', 'description': [['Prefix', '0x66'], ['Opcode', '0xA1'], ['Displacement', '0x00403000']], 'command': 'MOV AX, U'},
    {'byte': '66F72D004030A1', 'description': [['Prefix', '0x66'],['Opcode', '0xF7'],['Mod R/M', '0x2D'], ['Displacement', '0x00403000']], 'command': 'IMUL V'},
    {'byte': '6689C3', 'description': [['Prefix', '0x66'],['Opcode', '0x89'], ['Mod R/M', '0xC3']], 'command': 'MOV BX, AX'},
    {'byte': '66A10040303F', 'description': [['Prefix', '0x66'], ['Opcode', '0xA1'], ['Displacement', '0x0040303F']], 'command': 'MOV AX, Z'},
    {'byte': '6629D8', 'description': [['Prefix', '0x66'],['Opcode', '0x29'], ['Mod R/M', '0xD8']], 'command': 'SUB AX, BX'},
    {'byte': '66F73D0040307D', 'description': [['Prefix', '0x66'],['Opcode', '0xF7'],['Mod R/M', '0x3D'], ['Displacement', '0x0040307D']], 'command': 'IDIV W'},
    {'byte': '66030500403AFF', 'description': [['Prefix', '0x66'],['Opcode', '0x03'],['Mod R/M', '0x05'], ['Displacement', '0x00403AFF']], 'command': 'ADD AX, Y'},
    {'byte': '66A300402000', 'description': [['Prefix', '0x66'], ['Opcode', '0xA3'], ['Displacement', '0x00402000']], 'command': 'MOV X, AX'}]},

     {'name': 'Вычисление минимума и максимума в массиве',
      'desc': 'Для начала ..., далее приравниваем минимум и максимум к первому элементу массива. Каждый последующий элемент сравнивается со значением в регистрах, и, если подходит под условие максимума или минимума, то записывается в регистр.', 'example':
    [{'byte': '33F6', 'description': [['Opcode', '0x33'], ['Mod R/M', '0xF6']],'command': 'XOR ESI, ESI'},
     {'byte': 'A100403000', 'description': [['Opcode', '0xA1'], ['Displacement', '0x00403000']],'command': 'MOV EAX, [0x00403000]'},
     {'byte': '8B1D00403000', 'description': [['Opcode', '0x8B'], ['Mod R/M', '0x1D'],['Displacement', '0x00403000']],'command': 'MOV EBX, [0x00403000]'},
     {'byte': 'B900403000', 'description': [['Opcode', '0xB9'], ['Immediate', '0x00000003']],'command': 'MOV ECX, 3'},
     {'byte': 'EB58', 'description': [['Opcode', '0xEB'], ['Relative', '0x58']],'command': 'JMP [0x58]'},
     {'byte': '3B8600403000', 'description': [['Opcode', '0x3B'], ['Mod R/M', '0x86'],['Displacement', '0x00403000']],'command': 'CMP EAX, [0x00403000]'},
     {'byte': '741C', 'description': [['Opcode', '0x74'], ['Relative', '0x1C']],'command': 'JE [0x1C]'},
     {'byte': '3B8600403000', 'description': [['Opcode', '0x3B'], ['Mod R/M', '0x86'],['Displacement', '0x00403000']],'command': 'CMP EAX, [0x00403000]'},
     {'byte': '7C24', 'description': [['Opcode', '0x7C'], ['Relative', '0x24']],'command': 'JL [0x24]'},
     {'byte': 'EB00', 'description': [['Opcode', '0xEB'], ['Relative', '0x00']],'command': 'JMP [0x00]'},
     {'byte': '3B9E00403000', 'description': [['Opcode', '0x3B'], ['Mod R/M', '0x9E'],['Displacement', '0x00403000']],'command': 'CMP EBX, [0x00403000]'},
     {'byte': '7412', 'description': [['Opcode', '0x74'], ['Relative', '0x12']],'command': 'JE [0x12]'},
     {'byte': '7412', 'description': [['Opcode', '0x74'], ['Relative', '0x12']],'command': 'JE [0x12]'}]},

    {'name': 'Расчет гипотенузы',
     'desc': 'Загружаем вещественные значения и перемножаем с самим собой (а^2 и b^2), складываем два получившихся значения в стеке (а^2 и b^2), находим корень и сохраняем вещественное знаечние по заданному адресу.' ,'example':
   [{'byte': 'D90500402000', 'description': [['Opcode', '0xD9'], ['Mod R/M', '0x05'], ['Displacement', '0x00402000']], 'command': 'FLD [0x00402000]'},
    {'byte': 'D80D00402000', 'description': [['Opcode', '0xD8'], ['Mod R/M', '0x0D'], ['Displacement', '0x00402000']], 'command': 'FMUL [0x00402000]'},
    {'byte': 'D90500402004', 'description': [['Opcode', '0xD9'], ['Mod R/M', '0x05'], ['Displacement', '0x00402004']], 'command': 'FLD [0x00402004]'},
    {'byte': 'D80D00402004', 'description': [['Opcode', '0xD8'], ['Mod R/M', '0x0D'], ['Displacement', '0x00402004']], 'command': 'FMUL [0x00402004]'},
    {'byte': 'DEC1', 'description': [['Opcode', '0xDE'], ['Mod R/M', '0xC1']], 'command': 'FADDP ST(1), ST'},
    {'byte': 'D9FA', 'description': [['Opcode', '0xD9'], ['Mod R/M', '0xFA']], 'command': 'FSQRT'},
    {'byte': 'DB3D00402008', 'description': [['Opcode', '0xDB'], ['Mod R/M', '0x3D'], ['Displacement', '0x00403010']], 'command': 'FSTP [0x00402008]'}]},

    {'name': 'Нахождение площади треугольника',
     'desc': 'Загружаем вещественное число (угол между двумя сторонами), находим синус этого угла, домножаем на первую и на вторую сторону и делим на два. После, выгружаем ответ по заданному адресу из стека.' ,'example':
   [{'byte': 'D90500403008', 'description': [['Opcode', '0xD9'], ['Mod R/M', '0x05'], ['Displacement', '0x00402000']], 'command': 'FLD [0x00403008]'},
    {'byte': 'D9FE', 'description': [['Opcode', '0xD9'], ['Mod R/M', '0xFE']], 'command': 'FSIN'},
    {'byte': 'D80D00403000', 'description': [['Opcode', '0xD8'], ['Mod R/M', '0x0D'], ['Displacement', '0x00403000']], 'command': 'FMUL [0x00403000]'},
    {'byte': 'D80D00403004', 'description': [['Opcode', '0xD8'], ['Mod R/M', '0x0D'], ['Displacement', '0x00403004']], 'command': 'FMUL [0x00403004]'},
    {'byte': 'D8350040300C', 'description': [['Opcode', '0xD8'], ['Mod R/M', '0x35'], ['Displacement', '0x0040300C']], 'command': 'FDIV [0x0040300C]'},
    {'byte': 'DB3D00403010', 'description': [['Opcode', '0xDB'], ['Mod R/M', '0x3D'], ['Displacement', '0x00403010']], 'command': 'FSTP [0x00403010]'}]},


]

def get_examples_names():
    examples_names = []
    for example in examples:
        examples_names.append(example['name'])
    return examples_names

examples_names = get_examples_names()

