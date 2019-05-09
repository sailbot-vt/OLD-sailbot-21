import parse

class nmea():
    def __init__(self):
        self.format = "${0}*{1}\r\n"
    
    def parse(self, sentence):
        # pip install parse here.
        parsed = parse.parse(self.format, sentence)
        body = parsed[0]
        checksum = parsed[1]
        if self.checksum(body) == checksum:
            return body.split(',')
        return None

    def enable(self, sentence_ids=["ALL"], frequency=1):
        sentence_body = "PAMTC,EN,{0},1,{1},,"
        settings_sentences = []
        for sid in sentence_ids:
            settings_sentences.append(sentence_body.format(sid, frequency))
 
        output_sentences = []
        for body in settings_sentences:
            sent = "${0}*{1}\r\n".format(body, self.checksum(body))
            output_sentences.append(sent)

        return output_sentences

    def disable(self, sentence_ids=["ALL"], frequency=1):
        sentence_body = "PAMTC,EN,{0},0,{1},,"
        settings_sentences = []
        for sid in sentence_ids:
            settings_sentences.append(sentence_body.format(sid, frequency))
 
        output_sentences = []
        for body in settings_sentences:
            sent = "${0}*{1}\r\n".format(body, self.checksum(body))
            output_sentences.append(sent)

        return output_sentences


    def resume(self):
        body = "PAMTX,1"
        return "${0}*{1}\r\n".format(body, self.checksum(body))

    def pause(self):
        body = "PAMTX,0"
        return "${0}*{1}\r\n".format(body, self.checksum(body))

    def post(self):
        return "$PAMTC,POST*7F\r\n"

    def checksum(self, sentence):
        checksum = 0
        # XOR all characters in string
        for c in sentence:
            checksum = checksum ^ ord(c)

        return '{:x}'.format(checksum).upper()