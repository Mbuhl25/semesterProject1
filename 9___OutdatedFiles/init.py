#Init funktions


def averageList(matrix):
    '''
    This function returns the average values for multiple list in a new list.
    
    :param matrix: The matrix we want to calculate the average values from
    :type matrix: List of list
    
    :return average_list: A list with the average values

    '''
    
    average_list = []
    for i in range(len(matrix[0])):
        value = 0
        for x in range(len(matrix)):
            value += matrix[x][i]
        average_list.append(value / len(matrix))
    return average_list

def listSub(list1,list2):
    resultat = [x - y for x, y in zip(list1, list2)]
    return resultat

def listDiv(list1,list2):
    '''
    Dividing list1 with list2
    '''
    resultat = [x/y for x, y in zip(list1, list2)]
    return resultat


def norm(List,listmin,listmax):
    normlist = listDiv(listSub(List,listmin),listSub(listmax,listmin))
    return normlist

if __name__ == "__main__":
    list = [[1,4,3,4],[1,2,3,4]]
        
    print(listDiv([2,2,2],[1,1,1]))


    print(list[0][1])
    print(averageList(list))
