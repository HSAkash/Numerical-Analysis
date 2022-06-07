import imp
import re
import multiprocessing
import time

class SymbolTable:
    headers = [
        "stdio.h",
        "math.h",
        "conio.h",
        "stdlib.h",
        "string.h",
        "ctype.h",
        "time.h",
        "float.h",
        "limits.h",
        "wctype.h"
    ]

    Keywords = [
        "int",
        "int64",
        "float",
        "double",
        "char",
        "if",
        "while",
        "goto",
        "for"
    ]
    
    AOperator = [
        "+",
        "-",
        "*",
        "="
    ]

    IOperator = [
        "++",
        "--"
    ]

    LOperator = [
        "&&",
        "||",
        "!=",
        "==",
        "<",
        ">",
        "<=",
        ">=",
    ]

    Punctuation = [
        "(",
        ")",
        "[",
        "]",
        ",",
        ";",
        "\"",
        "'",
        "{",
        "}",
        "#"
    ]

class ContextFreeGrammar:
    Identifier = f"([a-z]|_)([a-z]|_|\d)*"
    IdentifierType = f"(int|int64|float|double|char)"
    Space = f"\s*"
    SpNew = f"({Space}\\n*)*"
    Equal = f"({Space}={Space})"
    ArithmaticOperator = f"({Space}(\+|-|\*|\\\){Space})"
    Identifier_Digit = f"({Identifier}|\d+)"
    VariableTypeValue = f"({Identifier}(|({Equal}{Identifier_Digit}(|({ArithmaticOperator}{Identifier_Digit})*))))"

    VariableDeclarationLine = f"({SpNew}{IdentifierType}{Space}{VariableTypeValue}(,{SpNew}{VariableTypeValue}{SpNew})*{SpNew})"
    VariableDeclarationFor = f"({SpNew}(|{IdentifierType}){SpNew}{VariableTypeValue}{SpNew})"
    VariableDeclarationMultiFor = f"({VariableDeclarationFor}(,{VariableDeclarationFor})*)"

    

    ValueInDecrement1 = f"((((\+\+)|(--)){Space}{Identifier})|({Identifier}{Space}((\+\+)|(--))))"
    ValueInDecrement2 = f"({Identifier}{Space}(\+|-)={Space}{Identifier_Digit}({Space}(\+|-){Space}{Identifier_Digit})*)"
    ValueInDecrement = f"({ValueInDecrement1}|{ValueInDecrement2})"
    ValueInDecrementFor = f"({ValueInDecrement}({SpNew},{SpNew}{ValueInDecrement})*)"
    


    PrintIdentifier = f"((,{SpNew}({VariableTypeValue}|{ValueInDecrement}){SpNew})*)"
    PrintLine = f"""({SpNew}printf{SpNew}\({SpNew}".*"{SpNew}{PrintIdentifier}\){SpNew})"""


    ConditionalExpression = f"({Identifier_Digit}{Space}((==)|<|>|(!=)|(>=)|(<=)){Space}{Identifier_Digit})"
    ConditionalExpressionFor = f"({SpNew}{ConditionalExpression}{SpNew}({SpNew},{SpNew}{ConditionalExpression})*{SpNew})"

    ForExpression = f"({SpNew}for{Space}\({SpNew}({VariableDeclarationMultiFor}|){SpNew};{SpNew}({ConditionalExpressionFor}|){SpNew};{SpNew}({ValueInDecrementFor}|){SpNew}\){SpNew})"
    IfExpression = f"{SpNew}if{Space}\({SpNew}{ConditionalExpressionFor}{SpNew}\){SpNew}"
    

    ReturnIdentifier = f"((,{SpNew}({VariableTypeValue}|{ValueInDecrement}|\d+){SpNew})*)"
    ReturnValue = f"""({SpNew}return{SpNew}(|(({SpNew}(\d+|{VariableTypeValue}|{ValueInDecrement}){SpNew}){ReturnIdentifier})){SpNew})"""
    

    # name
    # mainFunctionExpressiosn = ""
    # mainFunctionExpressions=f"({SpNew}/{mainFunctionExpressiosn}/{Space}{mainFunctionExpressiosn}h{mainFunctionExpressiosn}e{mainFunctionExpressiosn}m{mainFunctionExpressiosn}e{mainFunctionExpressiosn}l{mainFunctionExpressiosn}{Space}s{mainFunctionExpressiosn}h{mainFunctionExpressiosn}a{mainFunctionExpressiosn}r{mainFunctionExpressiosn}k{mainFunctionExpressiosn}e{mainFunctionExpressiosn}r{mainFunctionExpressiosn}{Space}a{mainFunctionExpressiosn}k{mainFunctionExpressiosn}a{mainFunctionExpressiosn}s{mainFunctionExpressiosn}h{mainFunctionExpressiosn}{Space}1{mainFunctionExpressiosn}7{mainFunctionExpressiosn}0{mainFunctionExpressiosn}1{mainFunctionExpressiosn}1{mainFunctionExpressiosn}6{mainFunctionExpressiosn})+"
    # name

    Lcurly='{'
    Rcurly='}'

    SetOfLine = f"({SpNew}({VariableDeclarationLine}|{PrintLine}|{ReturnValue}|{ValueInDecrementFor}|{VariableTypeValue}){SpNew};{SpNew})"

    CurlyBracketExpressionFor = f"({SpNew}{Lcurly}{SpNew}({SetOfLine})*{SpNew}{Rcurly}{SpNew})"
    ForFullExpression = f"({SpNew}{ForExpression}{SpNew}(;|{SetOfLine}|{CurlyBracketExpressionFor}){SpNew})"

    IfFullExpression = f"({SpNew}{IfExpression}{SpNew}(;|{SetOfLine}|{CurlyBracketExpressionFor}){SpNew})"

    CurlyBracketExpression = f"({SpNew}{Lcurly}{SpNew}({SetOfLine}|{ForFullExpression}|{IfFullExpression})*{SpNew}{Rcurly}{SpNew})"
    headers = "|".join(SymbolTable.headers)
    
    headerExpression = f"({SpNew}#{Space}include{Space}<({headers}){Space}>{SpNew})"
    mainFunctionExpression = f"({SpNew}int{SpNew}main{SpNew}\({SpNew}\){SpNew}{CurlyBracketExpression})"
    FullyExpression = f"({SpNew}({headerExpression})+{SpNew}{mainFunctionExpression}{SpNew})"




class Compiler:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = None
        self.index = 0
        self.token = {}
        self.dataLen = 0
        self.get_data()
        self.row = 0
        self.col = 0

    def get_data(self):
        data = None
        with open("code.txt", "r") as f:
            data = f.read()
        self.dataLen = len(data)
        self.data = data

    def cotation_data(self):
        index = self.index + 1
        token = {}
        token['type'] = "string"
        token['position'] = (self.row, self.col)
        data = '"'
        col = col + 1
        try:
            while self.data[index]:
                data += self.data[index]
                if data[index] == '"':
                    data += self.data[index]
                    token['data'] = data
                    return
            raise Exception(f"Line {self.row} Letter {self.col} {data}")
            
        except Exception as e:
            raise Exception(f"Line {self.row} Letter {self.col} {data} Not finished the line \".Cheak the code")
            

    def compileSub(self, pattern):
        print(f"""result: \n{re.findall(f"{pattern}", self.data)[0][0]}""")
        exit(1)

    def compile(self):
        pattern = ContextFreeGrammar.FullyExpression
        for x in range(len(ContextFreeGrammar.FullyExpression),0,-1):
            newPattern = pattern[:x]
            # proc = multiprocessing.Process(target=self.compileSub, args=(newPattern))
            # proc.start()
            # time.sleep(10)
            # proc.terminate()
            self.compileSub(newPattern)


        

        

txt = """
#include<stdio.h>

#include<math.h>
int main(){
    int a, b, c;

    
    for(a=1; a<5;a++){
        c = a + b;
        printf("%d",c);
    }

    for(; ;){
        c = a + b;
        printf("%d",c);
    }
    
    return 0;
}


"""
# # print(ContextFreeGrammar.Identifier)
# # print(ContextFreeGrammar.IdentifierType)
# # print(ContextFreeGrammar.Space)
# # print(ContextFreeGrammar.SpNew)
# # print(ContextFreeGrammar.Equal)
# # print(ContextFreeGrammar.ArithmaticOperator)
# # print(ContextFreeGrammar.VariableTypeValue)
# # print(ContextFreeGrammar.VariableDeclarationLine)
# # print(ContextFreeGrammar.ValueInDecrement1)
# # print(ContextFreeGrammar.ValueInDecrement2)
# # print(ContextFreeGrammar.ValueInDecrement)
# # print(ContextFreeGrammar.ValueInDecrementFor)
# # print(ContextFreeGrammar.ConditionalExpression)
# # print(ContextFreeGrammar.ConditionalExpressionFor)
# # print(ContextFreeGrammar.ForExpression)
# # print(ContextFreeGrammar.PrintLine)
# # print(ContextFreeGrammar.ReturnValue)
# # print(ContextFreeGrammar.SetOfLine)
# # print(ContextFreeGrammar.CurlyBracketExpression)
# # print(ContextFreeGrammar.ForFullExpression)
# # print(ContextFreeGrammar.CurlyBracketExpression)
# # print(ContextFreeGrammar.FullyExpression)
# print(re.findall(f"{ContextFreeGrammar.FullyExpression}", txt)[0][0])
# # data = "hemel"
# # print(data[:0])

# # compiler = Compiler("code.txt")
# # compiler.compile()

# print(re.findall(f"{ContextFreeGrammar.FullyExpression}", txt)[0][0])

def get_data_from_file(file_name='data.txt'):
    data = None
    with open(file_name, 'r') as file:
        data = file.read()
    data = re.sub(r'((\n\s)*//+.*\n)', '\n', data)
    # print(data)
    return data

data = get_data_from_file('data.txt')
print(re.findall(f"{ContextFreeGrammar.FullyExpression}", data)[0][0])

# import sys

# ret = {'foo': False, 'valid':False}
# def get_error(txt, grammer, queue):
#     try:

        
#         if (re.findall(f"{grammer}", txt)):
#             print(re.findall(f"{grammer}", txt)[0][0])
#             ret = queue.get()
#             ret['foo'] = True
#             # ret['valid'] = True
#             queue.put(ret)
#         else:
#             ret = queue.get()
#             ret['valid'] = True
#             queue.put(ret)
        
#     except:
#         pass
#         # exit(1)
#     # print(re.findall(f"{ContextFreeGrammar.FullyExpression}", txt)[0][0])

# # import timeit

# # start = timeit.default_timer()



# # stop = timeit.default_timer()

# # print('Time: ', stop - start)  



# # if __name__ == '__main__':
# #     # Start foo as a process
# #     grammer = ContextFreeGrammar.FullyExpression
# #     for x in range(len(grammer), 0, -1):
# #         print(x)
# #         queue = multiprocessing.Queue()
# #         queue.put(ret)
# #         p = multiprocessing.Process(target=get_error, name="get_error", args=(txt,grammer[:x], queue,))
# #         p.start()

# #         # Wait 10 seconds for foo
# #         time.sleep(.05)

# #         # Terminate foo
# #         p.terminate()

# #         # Cleanup
# #         p.join()
# #         if queue.get()['foo']:
# #             print(re.findall(f"{grammer[:x]}", txt)[0][0])
# #             break

# if __name__ == '__main__':
#     # Start foo as a process
#     grammer = ContextFreeGrammar.FullyExpression
#     for x in range(1,len(grammer)):
#         # print(x)
#         queue = multiprocessing.Queue()
#         ret['valid'] = False
#         queue.put(ret)
#         p = multiprocessing.Process(target=get_error, name="get_error", args=(txt,grammer[:x], queue,))
#         p.start()

#         # Wait 10 seconds for foo
#         time.sleep(.01)

#         # Terminate foo
#         p.terminate()

#         # Cleanup
#         p.join()
#         rrest = queue.get()
#         if rrest['foo']:
#             print(queue.get())
#             print(re.findall(f"{grammer[:x]}", txt)[0][0])
#             break
#         if rrest['valid']:
#             print(grammer[:x])
#             input('enterinput')


# # for x in range(len(ContextFreeGrammar.FullyExpression)-1, 0, -1):

# #     re.match(f"{ContextFreeGrammar.FullyExpression[:x]}", txt)

# # print(re.match(f"{ContextFreeGrammar.FullyExpression}", txt))