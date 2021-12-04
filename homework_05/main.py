import lightrdf as lightrdf


def get_all_super_topic_of(keyword):
    # parser = lightrdf.Parser()
    doc = lightrdf.RDFDocument('ontology.owl')
    for triple in doc.search_triples(None, None, None):
        if triple[2].endswith(keyword) and 'superTopicOf' in triple[1]:
            print(triple)


def main():
    keyword = input("Insert a word:")
    get_all_super_topic_of(keyword)


if __name__ == '__main__':
    main()
