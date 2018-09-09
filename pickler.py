import pickle
from os import listdir


def saveDataAsPickle(name, comments, tag, amount):
    file = open('./data/'+name+'.pickle', 'wb')
    try:
        pickle.dump({'comments': comments,
                     'tag': tag,
                     'amount': amount,
                     'name': name}, file)
        file.close()
        print('Saved: name: {0}, tag: {1}, amount: {2}\n'.format(
            name, tag, amount))
    except AttributeError:
        print('Wrong data type.')


def saveMultiple(data):
    try:
        for element in data:
            saveData(element['name'], element)
    except AttributeError:
        print('Wrong data type.')


def loadData(name):
    file = open('./data/'+name, 'rb')
    return pickle.load(file)


def loadAllFilesFromData():
    file_names = [file_name for file_name in listdir('./data') if '.pickle'
                  in file_name]
    return [loadData(file) for file in file_names]
