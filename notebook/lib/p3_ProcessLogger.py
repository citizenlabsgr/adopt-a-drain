import os
import os.path
class ProcessLogger:
    '''
    collects the process steps along the way
    then prints them
    '''
    def __init__(self,log_file_name=None):
        if log_file_name != None:
            self.file_name = log_file_name
        else:
            self.file_name = 'process.log'
        self.markdown_list = []

    def kill(self):

        if os.path.isfile(self.file_name):
            print('kill log: ',self.file_name)
            os.remove(self.file_name)
        else:
            print('no kill: ', self.file_name)
        return self

    def log(self, stringValue):
        with open(self.file_name, "a") as myfile:
            myfile.write(stringValue+'\n')
        return self

    def collect(self,markup):
        self.markdown_list.append(markup)
        return self

    def getMarkdown(self):
        return '\n'.join(self.markdown_list)

    def clear(self):
        self.markdown_list = []
        return self
    def show(self):
        print( self.markdown_list )

def main():
    pl = ProcessLogger()
    pl.kill()
    pl.log("HI")
    pl.log("Ho")


if __name__ == "__main__":
    # execute only if run as a script
    main()