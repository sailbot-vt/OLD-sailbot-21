import parse

class nmea():
    """ Defines nmea parser that can read, write, and parse nmea0183 sentences 

    Refer to 300 WX User Technical Manual_0183 for descriptions of fields
    """
    def __init__(self):
        """ Initializes an nmea parser 
        
        NMEA0183 sentence format: $<0:args>*<chksum>\r\n
        """
        self.nmea_format = "${0}*{1}\r\n"
    
    def parse(self, sentence, separator=','):
        """ Parses a given sentence

        Keyword arguments:
        sentence -- A string of a valid NMEA0183 sentence with valid checksum
            Precondition: start and line terminator must be included
        separator -- 
            The separator between each field in the nmea sentence. 
            Default: ','

        Returns:
        A list of data fields, where sentence id is first element.
        
        Note: Empty data fields == ''.
            Refer to 300WX User Technical Manual_0183 for detailed descriptions of
            data fields.
        """
        parsed = parse.parse(self.nmea_format, sentence)
        body = parsed[0]
        checksum = parsed[1]
        if self.checksum(body) == checksum:
            return body.split(separator)
        return None

    def toggle(self, sentence_ids=["ALL"], frequency=1, enable=1):
        """ Creates a sentence to toggle sentence(s) to be read in.
        
        Keyword arguments:
        setence_ids --
            A list of id's to enable/disable.
            Default: ["ALL"], to enable/disable all sentences
        frequency -- 
            seconds to wait before transmitting a sentence
            Default: 1 second
        enable --
            Enables or disable the given sentence id's from 
            transmitting. [1 = enable, 0 = disable]
            Default: 1

        Returns:
        The list of sentences to transmit to airmar to toggle sentence id
        """
        sentence_body = "PAMTC,EN,{0},{1},{2},,"
        settings_sentences = []
        for sid in sentence_ids:
            settings_sentences.append(sentence_body.format(sid, enable, frequency))
 
        output_sentences = []
        for body in settings_sentences:
            sent = self.nmea_format.format(body, self.checksum(body))
            output_sentences.append(sent)

        return output_sentences

    def power(self, resume=1):
        """ Creates a sentence to resume or pause data transmition

        Keyword Arguments:
        resume -- 1 to resume, 0 to pause

        Return:
        Sentence representing resume/pause
        """
        body = "PAMTX,{}".format(resume)
        return self.nmea_format.format(body, self.checksum(body))

    def post(self):
        """ Creates a sentence to perform POST (Power On Self Test)

        Return:
        Sentence representing POST for airmar.
        """
        body = "PAMTC,POST"
        return self.nmea_format.format(body, self.checksum(body))

    def factory_reset(self):
        """ Creates a sentence to factory reset

        Return:
        Sentence representing factory reset for airmar.
        """
        body = "PAMTX,1"
        return self.nmea_format.format(body, self.checksum(body))

    def checksum(self, sentence):
        """ Gets checksum for sentence body

        Keyword Arguments:
        sentence -- A valid nmea0183 sentence body (between '$' and '*')

        Returns:
        checksum for sentence body as uppercase hexcode.
        """
        checksum = 0
        # XOR all characters in string
        for c in sentence:
            checksum = checksum ^ ord(c)

        return '{:x}'.format(checksum).upper()