import lightrdf as lightrdf
import nltk
from nltk.stem import WordNetLemmatizer

ontology = lightrdf.RDFDocument('Resources/ontology.owl')


def get_all_super_topic_of():
    word = input("Insert a word: ")
    doc = lightrdf.RDFDocument('Resources/ontology.owl')
    for triple in doc.search_triples(None, None, None):
        extracted_first = str(triple[0])[::-1].split('/')[0][::-1]
        extracted_third = str(triple[0])[::-1].split('/')[0][::-1]

        if (extracted_first == word or extracted_third == word) and triple[1].endswith('superTopicOf'):
            print(triple)


def respects_rule_3(sentence):
    # VBP - verb
    # NN - noun
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    rule = 3
    for token in tagged_tokens:
        if rule == 3:
            if token[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                rule -= 1
        elif rule == 2:
            if token[1] in ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']:
                rule -= 1
        elif rule == 1:
            if token[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                return True
    return False


def respects_rule_4(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    for token in tagged_tokens:
        if token[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
            try:
                word = token[0]
                # wnl = WordNetLemmatizer()
                # word = wnl.lemmatize(token[0])
                # print(word)
                if exists_in_ontology(word):
                    print(word)
                    return True
            except:
                pass
    return False


def extract_fragments():
    f = open("Resources/sentences.txt", "r", encoding='utf8')
    data = f.readlines()
    output = open("Resources/sentences_Ontology_verified.txt", "a", encoding='utf8')
    for sentence in data:
        if sentence != r'\n':
            sentences = sentence.split('.')
            for s in sentences:
                if respects_rule_4(s):
                    output.write(s + '.')
            output.write('\n')


def extract_sentences():
    f = open("Resources/text.txt", 'r', encoding="utf8")
    data = f.readlines()
    output = open("Resources/sentences.txt", "a", encoding='utf8')
    for sentence in data:
        if sentence != '\n':
            sentence.replace('\n', '')
            sentences = sentence.split('.')
            for s in sentences:
                if s.startswith(' '):
                    s = s[1:]
                if respects_rule_3(s):
                    output.write(s + '.\n')


def exists_in_ontology(word):
    triples = ontology.search_triples(None, None, None)
    for triple in triples:
        if triple[0].endswith(word):
            return True


def main():
    # get_all_super_topic_of()
    extract_sentences()
    extract_fragments()


if __name__ == '__main__':
    main()
