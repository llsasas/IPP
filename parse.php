<?php

ini_set('display_errors', 'stderr');

$xml_output = "";

// Attaches given string to an output xml file that will be printed at the end of the program
function attach_to_output($current, $to_attach)
{
    fwrite(STDERR, "10");
    $current = $current . $to_attach . "\n";
    return $current;
}

// Prints the instruction how to use the program correctly if the --help is used
if ($argc > 1) {
    if ($argv[2] == "--help")
        echo ("Usage: parser.php "); //TODO
    exit(0);
}

$xml_output = attach_to_output($xml_output, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>");

// Erases the comments from the given line
function erase_comments($string)
{
    return preg_replace("/#.*/", '', $string);    
}

// Syntax check of variables
function is_variable($name)
{
    if (preg_match("/(LF | TF | GF)@([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?]))* /", $name)) {
        return 0;
    } else {
        return 23;
    }
}

function remove_whitespace($line)
{
    $pattern = '/[ \t]+/';
    $line = preg_replace($pattern, ' ', $line);
    $pattern = '/[ \t]+$/';
    $line = preg_replace($pattern, '', $line);
    return $line;
}

// Syntax check of labels
function is_label($name)
{
    fwrite(STDERR, "54");
    if (preg_match("/([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?]))* /", $name)) {
        return 0;
    } else {
        return 23;
    }
}

// Syntax check of symbols
function is_symbol($name)
{
    fwrite(STDERR, "65");
    if (preg_match("/(LF | TF | GF)@([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?])*) /", $name)) {
        return 0;
    }
    if (preg_match("/(bool)@(true | false) */", $name)) {
        return 0;
    }
    if (preg_match("/(int)@ [+-]?[0-9]* /", $name)) {
        return 0;
    }
    if (preg_match("/nil@nil/", $name)) {
        return 0;
    }
    //TODO finish string 
    if (preg_match("/string@([s]\\\\[0-9]{3}) /", $name)) {
        return 0;
    }

    return 23;
}

function is_type($name)
{
    fwrite(STDERR, "88");
    switch ($name) {
        case 'int':
        case 'bool':
        case 'string':
            return 0;
        default:
            return 23;
    }
}

function instruction($num, $tokens, $numofarguments, $argstype)
{
    fwrite(STDERR, "101");
    global $xml_output;
    $xml_output = attach_to_output($xml_output, "<instruction order=\"$num\" opcode=\"$tokens[0]\">");
    switch ($numofarguments) {
        case '1':
            $xml_output = attach_to_output($xml_output, "<arg1 type=\"$argstype[0]\">$tokens[1]</arg1>");
            break;
        case '2':
            $xml_output = attach_to_output($xml_output, "<arg1 type=\"$argstype[0]\">$tokens[1]</arg1>");
            $xml_output = attach_to_output($xml_output, "<arg2 type=\"$argstype[1]\">$tokens[2]</arg2>");
            break;
        case '3':
            $xml_output = attach_to_output($xml_output, "<arg1 type=\"$argstype[0]\">$tokens[1]</arg1>");
            $xml_output = attach_to_output($xml_output, "<arg2 type=\"$argstype[1]\">$tokens[2]</arg2>");
            $xml_output = attach_to_output($xml_output, "<arg3 type=\"$argstype[2]\">$tokens[3]</arg3>");
            break;
    }
    $xml_output = attach_to_output($xml_output, "</instruction>");
}

$header = false;
$instrctnum = 0;

while ($line = fgets(STDIN)) {
   $line = erase_comments($line);
   $line = remove_whitespace($line);
   $line = preg_replace("/&/",'&amp;',$line);                       #nacitanie po riadku zo vstupu, reg. vyrazy na upravu riadku (odkomentovanie, zamenenie zanakov)
   $line = preg_replace("/</",'&lt;',$line);
   $line = preg_replace("/>/",'&gt;',$line);
   $line = preg_replace('/#.*/','',preg_replace('#//.*#','',preg_replace('#/\*(?:[^*]*(?:\*(?!/))*)*\*//#','',($line))));
   
    if ($header == false && $line!= "\n") {
        if ((strtoupper(trim($line, "\n")) == ".IPPCODE23") || (strtoupper(trim($line, "\n")) == ".IPPCODE23")) {
            $header = true;
            $xml_output = attach_to_output($xml_output, "<program language=\"IPPcode23\">");
            continue;
        } 
        else 
        {
            exit(21);
        }
    }
    if($line == "\n")
    {
        continue;
    }
    $instrctnum++;
    $token = array_values(array_filter(explode(' ',trim($line, "\n"))));
    $arg_num = count($token) - 1;
    switch (strtoupper($token[0])) {
        // <var> <symb>
        case 'MOVE':
        case 'INT2CHAR':
        case 'STRLEN':
        case 'TYPE':
            $argstype = array("var", "symb");
            if($arg_num != 2)
            {
                exit(23);
            }
            if (!is_variable($token[1])) {
                if (is_symbol($token[2])) {
                    instruction($instrctnum, $token, $arg_num,$argstype);
                } else {
                    exit(23);
                }
            } else {

                exit(23);
            }

            break;

        // <var>
        case 'DEFVAR':
        case 'POPS':
            $argstype = array("var");
            if($arg_num != 1)
            {
                exit(23);
            }
            if (is_variable($token[1])) {
                instruction($instrctnum, $token, $arg_num,$argstype);
            } else {
                exit(23);
            }
            break;

        // <label>
        case 'CALL':
        case 'LABEL':
        case 'JUMP':
            $argstype = array("label");
            if($arg_num != 1)
            {
                exit(23);
            }
            if (is_label($token[1])) {
                instruction($instrctnum, $token, $arg_num,$argstype);
            } else {
                exit(23);
            }
            break;

        // <var> <symb1> <symb2>
        case 'ADD':
        case 'SUB':
        case 'MUL':
        case 'IDIV':
        case 'LT':
        case 'GT':
        case 'EQ':
        case 'AND':
        case 'OR':
        case 'NOT':
        case 'STRI2INT':
        case 'CONCAT':
        case 'GETCHAR':
        case 'SETCHAR':
            $argstype = array("var", "symb1", "symb2");
            if($arg_num != 3)
            {
                exit(23);
            }
            if (is_variable($token[1])) {
                if (is_symbol($token[2])) {
                    if (is_symbol(($token[3]))) {

                        instruction($instrctnum, $token, $arg_num,$argstype);
                    } else {
                        exit(23);
                    }
                } else {
                    exit(23);
                }
            } else {
                exit(23);
            }
            break;

        // <var> <type>
        case 'READ':
            $argstype = array("var", "type");
            if($arg_num != 2)
            {
                exit(23);
            }
            if (is_variable($token[1])) {
                instruction($instrctnum, $token, $arg_num,$argstype);
            } else {
                exit(23);
            }
            break;

        // <label> <symb1> <symb2>
        case 'JUMPIFEQ':
        case 'JUMPIFNEQ':
            $argstype = array("label", "symb1", "symb2");
            if($arg_num != 3)
            {
                exit(23);
            }
            if (is_label($token[1])) {
                if (is_symbol($token[2])) {
                    if (is_symbol(($token[3]))) {
                        instruction($instrctnum, $token, $arg_num,$argstype);
                    } else {
                        exit(23);
                    }
                } else {
                    exit(23);
                }
            } else {

                exit(23);
            }
            break;

        // <symb>
        case 'EXIT':
        case 'WRITE':
        case 'DPRINT':
        case 'PUSHS':
            $argstype = array("symb");
            if($arg_num != 1)
            {
                exit(23);
            }
            if (is_symbol($token[1])) {
                instruction($instrctnum, $token, $arg_num,$argstype);
            } else {
                exit(23);
            }
            break;
        default:
            exit(22); //TODO is this the correct return code for unknown instruction?
    }
}
$xml_output = attach_to_output($xml_output, "</program>");
echo($xml_output);

exit(0);

?>