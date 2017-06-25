import json
def returnKeywords(filename):
    keywords = []
    with open(filename) as data_file:
        data = json.load(data_file)

    for i in range(len(data)):
        keywords.append(str(data[i]['word']))

    return keywords
