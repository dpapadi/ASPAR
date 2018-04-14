import sys
from ParserClass import Parser

if __name__ == '__main__':

    in_file=open("/home/dpap/ASPAR/INPUT")
    my_parser = Parser(in_file)
    while True:
        docno = raw_input("\n\n\n\nPlease provide the docno of the document you wish to see or 0 to quit: ")
        if docno == '0':
            exit()
        else:
            print
            print my_parser.ret_doc(docno, 'text')
