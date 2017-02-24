PAGE = '網頁'
LIST = '清單'
APP = '應用程式'

def showConstants(request):
    context = {
        'PAGE':PAGE,
        'LIST':LIST,
        'APP':APP,
    }

    return context