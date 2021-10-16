import sys
import base64
class IO:
    @property
    def input(self):
        file_name = base64.b64decode(sys.argv[1].encode()).decode()
        with open(file_name,"rb") as file:
            file_content = file.read().decode()
        return file_content
    def output(self,output,part=None):
        if "2" in str(part):
            print('__AOC_CI_SYSTEM_OUTPUT_CALL_2:'+base64.b64encode(str(output).encode()).decode())
        else:
            print('__AOC_CI_SYSTEM_OUTPUT_CALL:'+base64.b64encode(str(output).encode()).decode())
io = IO()
