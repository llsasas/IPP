import sys
import xml.etree.ElementTree as ET
import re


# Trida urcena pro uchovavani dat o instrukci a zpristupnovani techto dat pomoci prislusnych metod
class Instruction:
    def __init__(self, arguments, opcode, instruction_info, order):
        self.arguments = arguments
        self.opcode = opcode
        self.instruction_info = instruction_info
        self.order = order

    def get_opcode(self):
        return self.opcode

    def get_argument_type(self, num):
        return self.arguments[num].attrib.get('type')

    def get_argument_text(self, num):
        return self.arguments[num].text


# Tato funkce slouzi ke kontrole argumentu programu
def arg_check():
    global source_file
    global input_file
    global inb
    global srcb
    argc = len(sys.argv)
    if argc > 3 or argc < 2:
        exit(10)

    for i in range(1, argc):
        arg = sys.argv[i]
        if arg == '--help' or arg == '-h':
            print('Usage: interpret.py --source --input')
            exit(0)
        elif arg.find('--source=') != -1:
            source_file = arg[9:]
            srcb = True
        elif arg.find('--input=') != -1:
            input_file = arg[8:]
            inb = True
        else:
            exit(10)


# Funkce slouzici ke kontrole hlavicky XML
def check_header(header):
    if header.tag != 'program':
        exit(32)

    if len(header.attrib) != 1:
        exit(32)
    elif header.attrib.get('language') is None:
        exit(32)
    elif header.attrib.get('language').upper() == '.IPPCODE23':
        exit(32)


# Funkce, ktera kontroluje jestli je type zapsan tak jak ma byt
def check_type(arg):
    if arg.attrib.get('type') != 'type':
        exit(32)
    elif arg.text not in ['int', 'string', 'bool', 'nil']:
        exit(32)


# Funkce, ktera kontroluje jestli je symbol zapsan tak jak ma byt
def check_symbol(arg):
    if arg.attrib.get('type') == 'var':
        check_var(arg)
    elif arg.attrib.get('type') == 'int':
        if not arg.text.isnumeric():
            exit(32)
    elif arg.attrib.get('type') == 'bool':
        if arg.text not in ['true', 'false']:
            exit(32)
    elif arg.attrib.get('type') == 'string':
        if arg.text is None:
            arg.text = ''
        elif not re.match(r'^((\\\d{3})|[^#\s\\])*$', arg.text):
            exit(32)
    elif arg.attrib.get('type') == 'nil':
        if arg.text != 'nil':
            exit(32)
    else:
        exit(32)


# Funkce, ktera kontroluje jestli je variable zapsana tak jak ma byt
def check_var(arg):
    if arg.attrib.get('type') != 'var':
        exit(32)
    if arg.text.find('@') != 1:
        splitted = arg.text.split('@', 1)
        if splitted[0] not in ['LF', 'TF', 'GF']:
            exit(32)
        if not re.match(r'^[_\-$#%*!?A-Za-z][A-Za-z\d_\-$#%*!?]*$', splitted[1]):
            exit(32)


# Funkce, ktera kontroluje jestli je label zapsan tak jak ma byt
def check_label(arg):
    if arg.attrib.get('type') != 'label':
        exit(32)
    if not re.match(r'^[_\-$#%*!?A-Za-z]([A-Za-z\d_\-$#%*!?])*$', arg.text):
        exit(32)


# Funkce ktera kontroluje pocet argumentu
def num_of_args(num1, num2):
    if num1 != num2:
        exit(32)


# Pomocna funkce pro kontrolu syntaxe XML
def check_syntax(arr):
    for i in range(0, len(arr)):
        ins = arr[i]
        # <var> < symb >
        if ins.opcode in ['MOVE', 'INT2CHAR', 'STRLEN', 'TYPE', 'NOT']:
            num_of_args(len(ins.arguments), 2)
            check_var(ins.arguments[0])
            check_symbol(ins.arguments[1])
        # <var>
        elif ins.opcode in ['DEFVAR', 'POPS']:
            num_of_args(len(ins.arguments), 1)
            check_var(ins.arguments[0])
        # <label>
        elif ins.opcode in ['CALL', 'LABEL', 'JUMP']:
            num_of_args(len(ins.arguments), 1)
            check_label(ins.arguments[0])
        # <var> <symb1> <symb2>
        elif ins.opcode in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'STRI2INT', 'CONCAT', 'GETCHAR',
                            'SETCHAR']:
            num_of_args(len(ins.arguments), 3)
            check_var(ins.arguments[0])
            check_symbol(ins.arguments[1])
            check_symbol(ins.arguments[2])
        # <var> <type>
        elif ins.opcode in ['READ']:
            num_of_args(len(ins.arguments), 2)
            check_var(ins.arguments[0])
            check_type(ins.arguments[1])
        # <label> <symb1> <symb2>
        elif ins.opcode in ['JUMPIFEQ', 'JUMPIFNEQ']:
            num_of_args(len(ins.arguments), 3)
            check_label(ins.arguments[0])
            check_symbol(ins.arguments[1])
            check_symbol(ins.arguments[2])
        # <symb>
        elif ins.opcode in ['EXIT', 'WRITE', 'DPRINT', 'PUSHS']:
            num_of_args(len(ins.arguments), 1)
            check_symbol(ins.arguments[0])
        # no arguments here, that is the only thing that we need to check here
        elif ins.opcode in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'RETURN', 'BREAK']:
            num_of_args(len(ins.arguments), 0)
        else:
            exit(32)


# Funkce ktera kontroluje instrukce
def check_instruction(instruction):
    tmp_arr = []
    for instarg in instruction:
        if not (instarg.tag != 'arg1' or instarg.tag != 'arg2' or instarg.tag != 'arg3'):
            exit(32)
        if instarg.attrib.get('type') is None:
            exit(32)
        elif instarg.attrib.get('type') not in ['label', 'var', 'nil', 'type', 'int', 'bool', 'string']:
            exit(32)
        tmp_arr.append(instarg)
    return tmp_arr


# Funkce ktera kontroluje XML soubor
def check_xml():
    global source_file
    srcf = source_file
    try:
        tree = ET.parse(srcf)
    except FileNotFoundError:
        exit(11)
    root = tree.getroot()
    check_header(root)
    bswitch = False
    instructions_array = []
    for child in root:
        if child.tag != 'instruction':
            exit(32)
        elif child.attrib.get('order') is None:
            exit(32)
        elif int(child.attrib.get('order')) <= 0:
            exit(32)
        elif child.attrib.get('opcode') is None:
            exit(32)
        bswitch = True
        arr = check_instruction(child)
        instructions_array.append(Instruction(arr, child.attrib.get('opcode'), child, child.attrib.get('order')))
    if bswitch:
        check_syntax(instructions_array)
    return instructions_array


# Funkce, ktera kontroluje a provadi instrukci move
def move(variable, symbolt, symbolvalue):
    global GF
    var_frame = variable[:2]
    var_name = variable[3:]

    s_type = symbolt
    if s_type == 'var':
        s_type, value = get_var_info(symbolvalue)
    else:
        value = symbolvalue

    if var_frame == 'GF':
        if var_name not in GF:
            exit(54)
        else:
            GF[var_name]['type'] = s_type
            GF[var_name]['value'] = value
    elif var_frame == 'LF':
        if len(LF) == 0:
            exit(55)
        if var_name not in LF[STACKTOP]:
            exit(54)
        LF[STACKTOP][var_name]['type'] = s_type
        LF[STACKTOP][var_name]['value'] = value

    elif var_frame == 'TF':
        if TF is None:
            exit(55)
        if var_name not in TF:
            exit(54)
        TF[var_name]['type'] = s_type
        TF[var_name]['value'] = value


# Funkce, ktera kontroluje a provadi instrukci PUSHFRAME
def pushframe():
    global TF
    global LF
    if TF is None:
        exit(55)
    else:
        LF.append(TF)
        TF = None


# Funkce, ktera kontroluje a provadi instrukci POPFRAME
def popframe():
    global TF
    global LF

    if len(LF) == 0:
        exit(53)
    TF = LF[STACKTOP]
    LF.pop()


# Funkce, ktera kontroluje a provadi instrukci DEFVAR
def defvar(var):
    var_frame = var[:2]
    var_name = var[3:]

    if var_frame == 'LF':
        if var_name in LF[STACKTOP]:
            exit(52)
        else:
            LF[STACKTOP][var_name] = {}
            LF[STACKTOP][var_name]['type'] = None
            LF[STACKTOP][var_name]['value'] = None

    elif var_frame == 'TF':
        if var_name in TF:
            exit(52)
        else:
            TF[var_name] = {}
            TF[var_name]['type'] = None
            TF[var_name]['value'] = None
    elif var_frame == 'GF':
        if var_name in GF:
            exit(52)
        else:
            GF[var_name] = {}
            GF[var_name]['type'] = None
            GF[var_name]['value'] = None


# Funkce, ktera kontroluje a provadi instrukci RETURN
def returnfc():
    global labelstack
    if len(labelstack) == 0:
        exit(56)
    returnval = labelstack[STACKTOP]
    labelstack.pop()
    return returnval


# Funkce, ktera kontroluje a provadi aritmeticke instrukce ADD,SUB,MUL a IDIV
def arithmetics(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = instrct.get_argument_text(1)
        if type1 == 'int':
            value1 = int(value1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = instrct.get_argument_text(2)
        if type2 == 'int':
            value2 = int(value2)

    if type1 != 'int' or type2 != 'int':
        exit(53)
    if instrct.opcode == 'ADD':
        move(instrct.get_argument_text(0), 'int', value1 + value2)
    elif instrct.opcode == 'SUB':
        move(instrct.get_argument_text(0), 'int', value1 - value2)
    elif instrct.opcode == 'MUL':
        move(instrct.get_argument_text(0), 'int', value1 * value2)
    elif instrct.opcode == 'IDIV':
        if int(value2) == 0:
            exit(57)
        move(instrct.get_argument_text(0), 'int', value1 / value2)


# Funkce, ktera kontroluje a provadi instrukce LT a EQ
def cmp(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = instrct.get_argument_text(1)
        if type1 == 'int':
            value1 = int(value1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = instrct.get_argument_text(2)
        if type2 == 'int':
            value2 = int(value2)
    if instrct.opcode in ['LT', 'GT']:
        if type1 != type2:
            exit(53)
        elif type1 not in ['bool', 'int', 'string']:
            exit(53)
        elif type2 not in ['bool', 'int', 'string']:
            exit(53)

    if instrct.opcode == 'LT':
        if value1 < value2:
            move(instrct.get_argument_text(0), 'bool', 'true')
        else:
            move(instrct.get_argument_text(0), 'bool', 'false')
    elif instrct.opcode == 'GT':
        if value1 > value2:
            move(instrct.get_argument_text(0), 'bool', 'true')
        else:
            move(instrct.get_argument_text(0), 'bool', 'false')
    elif instrct.opcode == 'EQ':
        if type1 != 'nil' and type2 != 'nil':
            if type1 != type2:
                exit(53)
        if value1 == value2:
            move(instrct.get_argument_text(0), 'bool', 'true')
        else:
            move(instrct.get_argument_text(0), 'bool', 'false')


# Funkce, ktera kontroluje a provadi logicke instrukce AND a OR
def logical(instrct):
    if instrct.opcode in ['AND', 'OR']:
        type1 = instrct.get_argument_type(1)
        if type1 == 'var':
            type1, value1 = get_var_info(instrct.get_argument_text(1))
        else:
            value1 = instrct.get_argument_text(1)
        type2 = instrct.get_argument_type(2)
        if type2 == 'var':
            type2, value2 = get_var_info(instrct.get_argument_text(2))
        else:
            value2 = instrct.get_argument_text(2)

        if type1 != 'bool' or type2 != 'bool':
            exit(53)

        if instrct.opcode == 'AND':
            if value1 == 'true' and value2 == 'true':
                move(instrct.get_argument_text(0), 'bool', 'true')
            else:
                move(instrct.get_argument_text(0), 'bool', 'false')
        elif instrct.opcode == 'OR':
            if value1 == 'false' and value2 == 'false':
                move(instrct.get_argument_text(0), 'bool', 'false')
            else:
                move(instrct.get_argument_text(0), 'bool', 'true')
    else:
        type1 = instrct.get_argument_type(1)
        if type1 == 'var':
            type1, value1 = get_var_info(instrct.get_argument_text(1))
        else:
            value1 = instrct.get_argument_text(1)
        if type1 != 'bool':
            exit(53)
        if value1 == 'false':
            move(instrct.get_argument_text(0), 'bool', 'true')
        else:
            move(instrct.get_argument_text(0), 'bool', 'false')


# Funkce, ktera kontroluje a provadi instrukci NOT
def notinstrc(instrct):
    type1 = instrct.get_argument_type(1)
    value1 = instrct.get_argument_text(1)
    if type1 != 'bool':
        exit(53)
    if value1 == 'true':
        move(instrct.get_argument_text(0), 'bool', 'false')
    else:
        move(instrct.get_argument_text(0), 'bool', 'true')


# Funkce, ktera kontroluje a provadi instrukci CONCAT
def concatinstrc(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = instrct.get_argument_text(1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = instrct.get_argument_text(2)

    if type1 != 'string' or type2 != 'string':
        exit(53)

    move(instrct.get_argument_text(0), 'string', value1 + value2)


# Funkce, ktera kontroluje a provadi instrukci STRLEN
def strlen(instrct):
    i_type = instrct.get_argument_type(1)
    if i_type == 'var':
        i_type, value = get_var_info(instrct.get_argument_text(1))
    else:
        value = instrct.get_argument_text(1)

    if i_type != 'string':
        exit(53)
    move(instrct.get_argument_text(0), 'int', len(value))


# Funkce, ktera kontroluje a provadi instrukce JMPIFEQ a JMPIFNEQ
def jmpifeqneq(instrct, labelsa):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = instrct.get_argument_text(1)
        if type1 == 'int':
            value1 = int(value1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = instrct.get_argument_text(2)
        if type2 == 'int':
            value2 = int(value2)

    if instrct.opcode == 'JUMPIFEQ':
        if (type1 == type2) or (type1 == 'nil' or type2 == 'nil'):
            if value1 == value2:
                rtrn = jump(instrct.get_argument_text(0), labelsa)
                return rtrn
            else:
                rtrn = -1
                return rtrn
        else:
            exit(53)
    elif instrct.opcode == 'JUMPIFNEQ':
        if (type1 == type2) or (type1 == 'nil' or type2 == 'nil'):
            if value1 != value2:
                rtrn = jump(instrct.get_argument_text(0), labelsa)
                return rtrn
            else:
                return -1
        else:
            exit(53)


# Funkce, ktera provadi instrukci PUSH
def pushs(instrct):
    global datastack
    type1 = instrct.get_argument_type(0)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(0))
    else:
        value1 = instrct.get_argument_text(0)
    datastack.append([type1, value1])


# Funkce, ktera kontroluje a provadi instrukci POPS
def pops(instrct):
    global datastack
    if len(datastack) == 0:
        exit(56)
    element = datastack.pop()
    move(instrct.get_argument_text(0), element[0], element[1])


# Funkce, ktera kontroluje a provadi instrukci JUMP
def jump(labelname, labels_l):
    if labelname in labels_l:
        next_instruction = labels_l[labelname]
        return next_instruction
    else:
        exit(52)


# Funkce, ktera kontroluje a provadi instrukci EXIT
def exit_instrct(num):
    if num in range(0, 49):
        exit(num)
    else:
        exit(57)


# Funkce, ktera kontroluje a provadi instrukci WRITE
def write_instrct(instrct):
    i_type = instrct.get_argument_type(0)
    if i_type == 'var':
        i_type, value = get_var_info(instrct.get_argument_text(0))
    else:
        value = instrct.get_argument_text(0)
    if i_type in ['int', 'string', 'bool']:
        print(value, end='')
    elif i_type == 'nil':
        print('', end='')


# Funkce, ktera kontroluje a provadi instrukci STR2INT
def str2int(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, tmparray = get_var_info(instrct.get_argument_text(1))
    else:
        tmparray = instrct.get_argument_text(1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, index = get_var_info(instrct.get_argument_text(2))
    else:
        index = int(instrct.get_argument_text(2))
    if type1 != 'string' or type2 != 'int':
        exit(53)
    if index < 0 or index > len(tmparray):
        exit(58)
    vardefined(instrct.get_argument_text(0))
    move(instrct.get_argument_text(0), 'int', ord(tmparray[index]))


# Funkce, ktera kontroluje a provadi instrukci INT2CHAR
def int2char(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value = get_var_info(instrct.get_argument_text(1))
    else:
        value = int(instrct.get_argument_text(1))
    if type1 != 'int':
        exit(53)
    vardefined(instrct.get_argument_text(0))
    try:
        value = chr(value)
        move(instrct.get_argument_text(0), 'string', value)
    except:
        exit(58)


# Funkce , ktera kontroluje jestli je variable definovana
def vardefined(var):
    global TF
    varframe = var[:2]
    varname = var[3:]

    if varframe == 'TF':
        if TF is None:
            exit(55)
        elif varname not in TF:
            exit(54)
    elif varframe == 'GF':
        if varname not in GF:
            exit(54)

    elif varframe == 'LF':
        if len(LF) == 0:
            exit(55)
        if varname not in LF[STACKTOP]:
            exit(54)

    elif varframe == 'TF':
        if TF is None:
            exit(55)
        if varname not in TF:
            exit(54)


# Funkce, ktera se pouziva k ziskani typu variable a jeji hodnoty
def get_var_info(var):
    vardefined(var)
    varframe = var[:2]
    varname = var[3:]
    vartype = None
    varvalue = None

    if varframe == 'TF':
        vartype = TF[varname]['type']
        varvalue = TF[varname]['value']
    if varframe == 'GF':
        vartype = GF[varname]['type']
        varvalue = GF[varname]['value']

    elif varframe == 'LF':
        vartype = LF[STACKTOP][varname]['type']
        varvalue = LF[STACKTOP][varname]['value']

    elif varframe == 'TF':
        vartype = TF[varname]['type']
        varvalue = TF[varname]['value']
    if vartype == 'int':
        varvalue = int(varvalue)
    return vartype, varvalue


# # Funkce, ktera kontroluje a provadi instrukci TYPE
def typeinstrct(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 in ['int', 'bool', 'string', 'nil']:
        move(instrct.get_argument_text(0), 'string', type1)
    if type1 == 'var':
        vartype, varvalue = get_var_info(instrct.get_argument_text(1))
        if vartype is None:
            move(instrct.get_argument_text(0), 'string', '')
        else:
            move(instrct.get_argument_text(0), 'string', vartype)


# Funkce, ktera kontroluje a provadi instrukci GETCHAR
def getchar(instrct):
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = instrct.get_argument_text(1)
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = int(instrct.get_argument_text(2))

    if type1 != 'string' or type2 != 'int':
        exit(53)
    if value2 < 0 or value2 > len(value1):
        exit(58)
    var = instrct.get_argument_text(0)
    vardefined(var)
    input_ch = value1[value2]
    move(var, 'string', input_ch)


# Funkce, ktera kontroluje a provadi instrukci SETCHAR
def setchar(instrct):
    var = instrct.get_argument_text(0)
    vartype, varval = get_var_info(var)
    type1 = instrct.get_argument_type(1)
    if type1 == 'var':
        type1, value1 = get_var_info(instrct.get_argument_text(1))
    else:
        value1 = int(instrct.get_argument_text(1))
    type2 = instrct.get_argument_type(2)
    if type2 == 'var':
        type2, value2 = get_var_info(instrct.get_argument_text(2))
    else:
        value2 = instrct.get_argument_text(2)

    if vartype != 'string' or type1 != 'int' or type2 != 'string':
        exit(53)
    if value1 < 0 or value2 == '' or value1 > len(varval):
        exit(58)
    vardefined(var)
    strings = list(varval)
    strings[value1] = value2
    strings = ''.join(strings)
    move(var, 'string', strings)


# Funkce, ktera provadi instrukci READ
def readinstrc(instrct):
    global input_file
    variable = instrct.get_argument_text(0)
    type1 = instrct.get_argument_text(1)
    if input_file == sys.stdin:
        try:
            value = input()
            value = value.split('\n')[0]
        except:
            move(variable, 'nil', 'nil')
            return
    else:
        try:
            value = input_file.readline()
            value = value.split('\n')[0]
        except:
            move(variable, 'nil', 'nil')
    if type1 == 'bool':
        if value.upper() == 'FALSE':
            move(variable, 'bool', 'false')
        else:
            move(variable, 'bool', 'true')
    elif type1 == 'int':
        move(variable, 'int', value)
    elif type1 == 'string':
        move(variable, 'string', value)


# Funkce, ktera se pouziva jako switch
def switchfnct(instruct):
    global i
    global labelstack
    global TF
    if instruct.opcode == 'MOVE':
        move(instruct.get_argument_text(0), instruct.get_argument_type(1), instruct.get_argument_text(1))
    elif instruct.opcode == 'PUSHFRAME':
        pushframe()
    elif instruct.opcode == 'POPFRAME':
        popframe()
    elif instruct.opcode == 'CREATEFRAME':
        global TF
        TF = {}
    elif instruct.opcode == 'DEFVAR':
        defvar(instruct.get_argument_text(0))
    elif instruct.opcode == 'CALL':
        labelstack.append(i)
        i = jump(instruct.get_argument_text(0), labels)
    elif instruct.opcode == 'RETURN':
        if len(labelstack) != 0:
            i = labelstack[STACKTOP]
            labelstack.pop()
        else:
            exit(56)
    elif instruct.opcode == 'PUSHS':
        pushs(instruct)
    elif instruct.opcode == 'POPS':
        pops(instruct)
    elif instruct.opcode in ['ADD', 'SUB', 'MUL', 'IDIV']:
        arithmetics(instruct)
    elif instruct.opcode in ['LT', 'GT', 'EQ']:
        cmp(instruct)
    elif instruct.opcode in ['AND', 'OR', 'NOT']:
        logical(instruct)
    elif instruct.opcode == 'INT2CHAR':
        int2char(instruct)
    elif instruct.opcode == 'STRI2INT':
        str2int(instruct)
    elif instruct.opcode == 'READ':
        readinstrc(instruct)
    elif instruct.opcode == 'WRITE':
        write_instrct(instruct)
    elif instruct.opcode == 'CONCAT':
        concatinstrc(instruct)
    elif instruct.opcode == 'STRLEN':
        strlen(instruct)
    elif instruct.opcode == 'GETCHAR':
        getchar(instruct)
    elif instruct.opcode == 'SETCHAR':
        setchar(instruct)
    elif instruct.opcode == 'TYPE':
        typeinstrct(instruct)
    elif instruct.opcode in ['LABEL', 'DPRINT', 'BREAK']:
        pass
    elif instruct.opcode == 'JUMP':
        i = jump(instruct.get_argument_text(0), labels)
    elif instruct.opcode == 'EXIT':
        if instruct.get_argument_type(0) != 'int':
            exit(53)
        exit_instrct(int(instruct.get_argument_text(0)))
    elif instruct.opcode in ['JUMPIFEQ', 'JUMPIFNEQ']:
        val = jmpifeqneq(instruct, labels)
        if val != -1:
            i = val


# Hlavni program
srcb = False
inb = False
arg_check()
if not srcb:
    source_file = sys.stdin.readlines()
if not inb:
    input_file = sys.stdin
if input_file != sys.stdin:
    input_file = open(input_file, 'r')
instructions = check_xml()
labels = {}
STACKTOP = - 1
labelstack = []
datastack = []
LF = []
GF = {}
TF = None
i = 0

# For cyklus pro ulozeni labels
for i in range(0, len(instructions)):
    ins = instructions[i]
    if ins.opcode == 'LABEL':
        label_n = ins.get_argument_text(0)
        if label_n in labels:
            exit(52)
        else:
            labels[label_n] = i
# While cyklus urceny pro iteraci vsemi instrukcemi a jejich provedeni
i = 0
while i < len(instructions):
    instr = instructions[i]
    switchfnct(instr)
    i = i + 1
