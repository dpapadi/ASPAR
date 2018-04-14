class Parser:

    input_file = None   #input file
    __content = ""        # input file as string
    __doc_dict = {}       #dictionaty to store doc info
    __sec_id = [ 'doc', 'docno', 'docid', 'date', 'section', 'length', 'headline', 'byline', 'text', 'graphic', 'type' ]


    def __init__(self, infile):
        print "Class init\n"
        self.input_file = infile
        self.__content = self.input_file.read()
        self.input_file.close()
        self.__main_process()
        print self.__doc_dict
        (i, ii) = self.__doc_dict['LA010189-0013']['date'][1]
        print self.__content[i:ii]


    def __main_process(self):
        #self.content = self.input_file.read()
        begin = 0   # the beginning of every ection
        end = 0     # the end of every section     
        st = 0
        en = 0
        stop = False
        i = 1
        while not stop:
            cur_docno = ""
            for sid in self.__sec_id:
                if sid == 'doc':
                    (begin, end) = self.__get_sec(self.__content[st:], sid , st)
                    st = begin  # index of the begin of the <doc> of the iteration
                    en = end    # index of the end of the <doc> of the iteration
                    if st == -1 or en == -1:
                        stop = True
                        break
                else:
                    (begin, end) = self.__get_sec(self.__content[st:en], sid, st)
                    if sid == 'docno':
                        cur_docno = self.__content[begin:end]
                        #print cur_docno
                    if end != -1:
                        st = end
                    self.__store_sec(self.__content, sid, cur_docno, begin, end)
                #print sid + "\n" + self.content[begin:begin+6] + "\t" + self.content[end:end+6]
                #print str(begin) + "\t" + str(end)
            if cur_docno != "":
                self.__doc_dict[cur_docno]['position'] = i
            i += 1

    def __get_sec(self, text, sec_id, con):
        ####################
        # 
        # returns the indexes that contain the
        # section of the text
        # related to the sec_id inside content string
        #
        ####################
        start = '<' + sec_id + '>'
        end = '</' + sec_id + '>'
        i = text.find(start)  
        #raw_input()
        ii = text[i:].find(end)
        if i == -1 or ii == -1:
            return (i, ii)
        #return (text[i+len(start):ii-1], end+1)
        return (i + len(start)+ con +1, i + ii - 1 + con)

    def __store_sec(self, text, sid, doc_no, start, stop):
        #####################
        #
        # stores the indexes of every section 
        # in the doc_dict dictionary 
        # grouped by docno of every document
        #
        #####################
        if sid == 'docno':
            self.__doc_dict[doc_no] = {}
        else:
            i = text[start:stop].find('<p>')
            if i == -1:
                self.__doc_dict[doc_no][sid] = (start, stop)
                return
            else:
                par_no = 1 # paragraph number     
                while True:
                    ####################
                    #
                    # discover and store 
                    # seperate paragraphs
                    #
                    ####################
                    i = text[start:stop].find('<p>')
                    #print i
                    #raw_input()
                    ii = text[i+start+4:stop].find('</p>')
                    if i == -1 or ii == -1:
                        break
                    else:
                        i += 4 + start
                        ii += i -1
                        if sid not in self.__doc_dict[doc_no]:
                            self.__doc_dict[doc_no][sid] = {}
                        self.__doc_dict[doc_no][sid][par_no] = (i, ii)
                        start = ii
                        par_no += 1
                    
    def ret_doc(self, docno, sec): #TODO
        ret = ""
        temp = ""
        i = 1
        #for sid in self.__sec_id:
        while True:
            if i in self.__doc_dict[docno]['text']:
                (begin, end) = self.__doc_dict[docno]['text'][i]
                ret += self.__content[begin:end] + "\n"
                i+=1
            else:
                break
        return ret


    def test(self):
        print "Testing"
        print self.input_file
        return self.input_file
