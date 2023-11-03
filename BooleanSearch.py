import json
import time

with open('news.json') as file:
    corpus = file.read()

def create_index(corpus):

    index = {}
    for doc_id, document in enumerate(corpus):
        terms = document.lower().split()
        for term in terms:
            if term not in index:
                index[term] = []
            if doc_id not in index[term]:
                index[term].append(doc_id)
    return index


def splitLinksDescs(file_name):
    corpus = []
    links = []
    with open(file_name) as file:
        for row in file:
            links.append(json.loads(row)['short_description'])
            corpus.append(json.loads(row)['link'])
    return corpus, links


def boolean_search(inverted_index, query):
    words = query.lower().split()
    result = set()
    for i in words:
        split_word = i.split("&")
        if split_word[0] in inverted_index:
            temp = set(inverted_index[split_word[0]])
        else:
            temp = set()

        for j in split_word[1:]:
            if j in inverted_index:
                temp = temp.intersection(inverted_index[j])
            else:
                temp = set()
                break
        result = result.union(temp)

    return result


links, descriptions = splitLinksDescs(file_name='./news.json')
inv_index = create_index(corpus=descriptions)

Result = []
QUERIES = ("BMW", "mountain", "london", "school teacher", "washington dc")
start = time.time()

for i in range(len(QUERIES)):
    Result.append(boolean_search(QUERIES[i], inv_index))

end = time.time()
totalTime = ((end - start)* 10 ** 6)

print(f'Time to search {len(QUERIES)} quiries: {totalTime} micro seconds \n avg time: {totalTime/5} micro seconds')
for i, r in enumerate(Result):
    print(f'number of results: {len(r)}, for query ({QUERIES[i]})')
    r = list(r)
    for j in range(len(QUERIES) if len(r) > len(QUERIES) else len(r)):
        print(f'link {j + 1}: {links[r[j]]} \ndescription:\n{descriptions[r[j]]} \n')

