import matplotlib.pyplot as plt

class Node:
    # object were data is stored in the LinkedList
    # the Node contains the word count (word_cnt) and the document id of the doc (doc_id)
    def __init__(self, doc_id = None, word_cnt = None):
        self.doc_id = doc_id
        self.word_cnt = word_cnt
        self.next_node = None

class LinkedList:
    
    def __init__(self, head = None):
        # initialize by giving the head of the list or None if the list is empty
        self.head = head
        self.last_node = head

    def insert(self, doc_id, word_cnt):
        new_node = Node(doc_id, word_cnt)
        if self.head == None:
            self.head = new_node
            self.last_node = new_node
        else:
            self.last_node.next_node = new_node
            self.last_node = new_node

    def search(self, doc_id):
        tmp = self.head
        found = False
        while tmp:
            print tmp.word_cnt
            if tmp.doc_id == doc_id:
                return tmp
            else:
                tmp = tmp.next_node
        raise ValueError("doc_id not in LinkedList")

class Parser:

    #from . import LinkedList
    input_file = None   #input file
    __content = ""        # input file as string
    __doc_dict = {}       #dictionaty to store doc info
    __sec_id = [ 'doc', 'docno', 'docid', 'date', 'section', 'length', 'headline', 'byline', 'text', 'graphic', 'type' ]
    #words = {}
    __doc_array = []
    __hash_table = {}
    #created based on regular patterns of the english language; should be updated for more accuracy
    #NOTE: I do not check for different forms in verbs, as patters like ed or ing can indicate adjectives
    #       for this purpose, word tagging should be implimented
    __word_ending_patterns ={   's'     :   '',
                                'ss'    :   'ss',
                                'as'    :   'as',
                                'is'    :   'is',
                                'us'    :   'us',
                                'oes'   :   'o',
                                'ies'   :   'y',
                                'ves'   :   'f',
                                'ous'   :   'ous',
                                'sses'  :   'ss',
                                'xes'   :   'x',
                                'ches'  :   'ch',
                                'shes'  :   'sh',
                                'uses'  :   'us'

                            }
    # exceptions for the above rules
    __exceptions = {    'its'       :   'its',
                        'objectives':   'objective',
                        'lies'      :   'lie',
                        'yes'       :   'yes',
                        'observes'  :   'observe',
                        'moves'     :   'move',
                        'men'       :   'man',
                        'women'     :   'woman',
                        'childern'  :   'child',
                        'people'    :   'person',
                        'am'        :   'be',
                        'are'       :   'be',
                        'is'        :   'be',
                        'was'       :   'be',
                        'were'      :   'be'
                        }
    test = 0


    def __init__(self, infile):
        self.input_file = infile
        self.__content = self.input_file.read()
        self.input_file.close()
        self.__main_process()
        for i in range(len(self.__doc_array)): 
            self.__process_doc(self.ret_doc(i), i+1)
        print "\n\nINPUT collection has been parsed successfully!!!\n\n"


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
                self.__doc_array.append(cur_docno)
            i += 1
            #print self.__doc_array

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
                    
    def ret_doc(self, docno): #TODO
        ret = ""
        temp = ""
        i = 1
        #for sid in self.__sec_id:
        for sec_id in self.__sec_id:
            if sec_id == 'doc' or sec_id == 'docno' or sec_id == 'docid':
                continue
            elif isinstance(self.__doc_dict[self.__doc_array[docno]][sec_id], dict):
                while True:
                    if i in self.__doc_dict[self.__doc_array[docno]][sec_id]:
                        (begin, end) = self.__doc_dict[self.__doc_array[int(docno)]][sec_id][i]
                        ret += self.__content[begin:end] + "\n"
                        i+=1
                    else:
                        ret += "\n\n"
                        i = 1
                        break
            else:
                (begin, end) = self.__doc_dict[self.__doc_array[docno]][sec_id]
                ret += self.__content[begin:end] + "\n\n\n"
        #self.__process_doc(ret)
        return ret

    
    def __process_doc(self, text, docno = None):
        temp_word = ""
        temp_dict = {}
        count = 0
        for i in range(len(text)):
            ch = text[i]
            #print ch
            #raw_input()
            if ch.isalnum() or ch =="'" or  ch == "-":
                if ch.upper():
                    ch = ch.lower()
                temp_word += ch
            else:
                if temp_word != "":
                    count += 1
                    (proc_word, cnt_not) = self.__process_word(temp_word)
                    if cnt_not:
                        if 'not' not in temp_dict:
                            temp_dict['not'] = 1
                        else:
                            temp_dict['not'] += 1
                    if proc_word not in temp_dict:
                        temp_dict[proc_word] = 1
                    else:
                        temp_dict[proc_word] += 1
                temp_word = ""
                #raw_input()
        for word, cnt in temp_dict.items():
            hsh = hash(word)
            if hsh not in self.__hash_table:
                self.__hash_table[hsh] = LinkedList()
            self.__hash_table[hsh].insert(docno, cnt)
        return

    def __process_word(self, inpt):
        ############################
        #
        # before calculating the hash do a simple processing of the word to
        # to find simple word ending patterns that indicate plural or other forms
        # of the same word based on an preconfigured array. For more accuracy
        # add more expressions to the array, a library for irregular forms and impliment word tagging to 
        # discover the type of word ( noun, verb etc )
        #
        ###########################
        outpt = inpt
        count_not = False
        if outpt.startswith("'") and not outpt[1:].isdigit():
            outpt = outpt[1:]
        while outpt.endswith("'"):
            outpt = outpt[:-1]
        if outpt[-2:] == "'s":
            outpt = outpt[:-2]
        elif outpt[-3:] == "n't":
            outpt = outpt[:-3]
            if outpt == "ca":
                outpt = "can"
            count_not = True
        if outpt in self.__exceptions:
            outpt = self.__exceptions[outpt]
        elif outpt.endswith('s'):
            k = -4
            while k < 0:
                if outpt[k:] in self.__word_ending_patterns:
                    outpt = outpt[:k] + self.__word_ending_patterns[outpt[k:]]
                    break
                k += 1
        
        if outpt == 'the':
            self.test += 1
        return (outpt, count_not)

    def plot_count_dist(self):
        plot_data = {}
        for hsh, linked_list in self.__hash_table.items():
            total_count = 0
            node = linked_list.head
            while node != None:
                total_count += node.word_cnt
                node = node.next_node
            if total_count not in plot_data:
                plot_data[total_count] = 1
            else:
                plot_data[total_count] += 1
        plt.bar(plot_data.keys(), plot_data.values(), color='g')
        plt.show()


    def return_data(self):
        print '\n\n'
        print 'Enter:'
        for i in range(len(self.__doc_array)):
            print '%s\tfor article %s' %(i+1, self.__doc_array[i])
        print '0\tto return\n'
        choice = raw_input()    
        return choice
