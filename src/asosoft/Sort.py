def KurdishSort(inputList):
    ku = list("ئءاآأإبپتثجچحخدڎڊذرڕزژسشصضطظعغفڤقكکگڴلڵمنوۆۊۉۋهھەیێ")
    return CustomSort(inputList, ku)

def CustomSort(inputList, inputOrder):
    base_char = 62000
    order = [chr(base_char + i) for i in range(len(inputOrder))]
    for i in range(len(inputList)):
        for j in range(len(order)):
            inputList[i] = inputList[i].replace(inputOrder[j], order[j])
    inputList.sort()
    for i in range(len(inputList)):
        for j in range(len(order)):
            inputList[i] = inputList[i].replace(order[j], inputOrder[j])
    return inputList