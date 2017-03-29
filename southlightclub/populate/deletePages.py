from populate import base
from main.models import Page, ListItem


def deleteAll():
    print('Delete everything... ', end='')
    Page.objects.all().delete()
    ListItem.objects.all().delete()
    print('done.')


if __name__ == '__main__':
    deleteAll()





