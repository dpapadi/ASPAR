class Parser:

    input_file = None   #input file
    content = ""        # input file as string
    doc_dict = {}       #dictionaty to store doc info
    sec_id = [ 'doc', 'docno', 'docid', 'date', 'section', 'length', 'headline', 'byline', 'text', 'graphic', 'type' ]


    def __init__(self, infile):
        print "Class init"
        self.input_file = infile
        self.main_process()
    
    def main_process(self):
        self.content = self.input_file.read()
        temp = ""
        i = 0
        for sid in sec_id:
            (temp, i) = self.get_sec(self.content[i:], sid)

    def get_sec(self, text, sec_id):
        ####################
        # 
        # returns the section of the text 
        # that is related to the sec_id
        #
        ####################
        start = '<' + sec_id + '>'
        end = '</' + sec_id + '>'
        i = text.find(start)
        ii = text.find(end)
        return (text[i+len(start):ii-1], end+1)


    def test(self):
        print "Testing"
        print self.input_file
        return self.input_file
