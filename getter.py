from time import sleep
from facebook import GraphAPI

TOKEN = 'EAAFpZCp8376ABANHxBKhCyYgfBZAZBi6J41eE4UBJL2fkIZCRUFVI3KB0wM3ZAlli2KDi72bxYkTX89t2FNUiXKmQYbSDaBRnxg3Upmgh1hiJNZBnT2cby6tBg501RHDYh3uWZCCichnFGiATf7fJZAiCDAHKuKLTYWWsmwYOvukUQZDZD'


def get_name(id):
    """
    Get id's Facebook Name

    :param int id:
    :return: str
    """

    graph = GraphAPI(access_token=TOKEN, version='2.5')

    return graph.get_object(id=str(id).split('-')[0])['name']


def find_user(user, names):
    try:
        names.append(get_name(user))
    except:
        names.append(user + ' - Deleted account or you need to sign in to view their name')


if __name__ == '__main__':
    names = []
    users = []
    threads = []

    # Reads ids
    file = open('ids.txt', encoding='utf8')

    for lines in file.readlines():
        users += lines.strip('\n').split(',')

    file.close()

    ans = input('Do you want to multi-thread or single thread? ' +
                '(Single thread if you have a large list in case you get kicked off):\n')

    if 'multi' in ans:
        # If multi-threading is chosen
        import threading

        for user in range(len(users)):
            # Makes threads galore
            t = threading.Thread(target=find_user, args=(users[user].strip('"'), names))
            t.daemon = True
            t.start()
            threads.append(t)

        # Waits for multi-threads to all finish
        while any([x if x.isAlive() else threads.remove(x) for x in threads]):
            sleep(1)
    else:
        # If single-threading is chosen
        for user in range(len(users)):
            find_user(users[user].strip('"'), names)

    # Write all names into file
    file = open('id-to-names.txt', 'w')
    for name in names:
        file.write(name + '\n')
    file.close()
