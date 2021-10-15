import sys
import base64
class IO:
    @property
    def input(self):
        return base64.b64decode(sys.argv[1].encode()).decode()
    def output(self,output):
        print(base64.b64encode(str(output).encode()).decode())
io = IO()
