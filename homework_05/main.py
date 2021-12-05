import lightrdf as lightrdf
import nltk


def get_all_super_topic_of(keyword):
    # parser = lightrdf.Parser()
    keyword = input("Insert a word:")
    doc = lightrdf.RDFDocument('Resources/ontology.owl')
    for triple in doc.search_triples(None, None, None):
        if triple[2].endswith(keyword) and 'superTopicOf' in triple[1]:
            print(triple)


def extract_sentences():
    # f = open("Resources/text.txt", 'r')
    # data = f.readlines()
    data = "I bought milk yesterday"
    tokens = nltk.word_tokenize(data)
    tagged_tokens = nltk.pos_tag(tokens)
    print(tagged_tokens)


def main():
    # keyword = input("Insert a word:")
    # get_all_super_topic_of(keyword)
    extract_sentences()


if __name__ == '__main__':
    main()
