import sys
from ParserClass import Parser

if __name__ == '__main__':

    try:
        in_file=open(sys.argv[1])
    except:
        print "\nProvide a valid INPUT file!!\n"
        exit()
    my_parser = Parser(in_file)
    while True:
        try:
            choice = raw_input('\n\nEnter:\n1:\tto read a specific article\n2:\tto generate the word distribution plot\n0:\tto exit\n\n')
            if choice == '0':
                exit()
            elif choice == '2':
                my_parser.plot_count_dist()
            elif choice == '1':
                while True:
                    docseq = my_parser.return_data()
                    if docseq == '0':
                        break
                    else:
                        print my_parser.ret_doc(int(docseq)-1)
            else:
                raise Exception
        except Exception as e:
                print "WRONG INPUT\n"
                print 'DEBUG: ' 
                print e 
