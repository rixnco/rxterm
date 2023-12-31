from filters import FilterBase


class LVSVibrate(FilterBase):
    """Filter out Vibrate messages"""
    NAME = "lvs"

    def __init__(self, terminal, config):
        FilterBase.__init__(self,terminal,config)
        self.buffer=''
        self.vibe_idx=0
        

    def rx(self, text):
        res=''
        last = 0
        while True:
            idx = text.find("\n", last)
            if idx == -1:
                idx = text.find(";", last)
                if idx == -1:
                    if len(self.buffer) < 4096:
                        self.buffer += text[last:]
                    break
                line= self.buffer + text[last:idx+1]
                last = idx+1
                if line.endswith("Vibrate:0;"):
                    line=line[:-10]

                self.buffer=''
                res+=line
            else:
                line= self.buffer + text[last:idx+1]
                if line.endswith("Vibrate:0;\n"):
                    line=line[:-11]
                self.buffer=''
                last = idx+1
                res+=line
                

        return res


    def tx(self, text):
        return text