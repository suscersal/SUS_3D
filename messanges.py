from termcolor import colored,cprint





def warn(data):
    cprint(data,None,'on_yellow')

def error(data):
    cprint(data,None,'on_red')

def succes(data):
    cprint(data,None,'on_green')

# warn('warn')
# error('error')
# succes('succes')