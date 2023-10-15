import urllib.request
import xml.etree.ElementTree as ET
import joblib

memory = joblib.Memory(location='cache', verbose=0)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}


@memory.cache()
def load_xml(url, cache=True):
    if not cache:
        memory.clear()
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    if response.getcode() != 200:
        raise Exception(f"Error {response.getcode()} when loading {url}")
    xml = response.read()
    return ET.fromstring(xml)


def thesaurus_uris(cache=True):
    tree = load_xml("http://publications.europa.eu/resource/dataset/eurovoc", cache)
    return {int(r.attrib['thesaurus_id']): r.attrib['thesaurus_uri']
            for r in tree.findall(".//record[@thesaurus_id]") if r.attrib['thesaurus_id'] != ''}


def thesaurus_en_labels(cache=True):
    def _thesaurus_en_labels():
        for k, v in thesaurus_uris(cache).items():
            tree = load_xml(v, cache)
            node = tree.find(".//dcterms:title[@xml:lang='en']",
                             {'dcterms': "http://purl.org/dc/terms/",
                              "xml": "http://www.w3.org/XML/1998/namespace"})
            label = node.text.replace(str(k), '').strip()
            if label.startswith('0 '):
                label = label[2:]
            yield k, label

    return dict(_thesaurus_en_labels())


class Eurovoc:
    def __init__(self, cache=True, lang='en'):
        assert lang == 'en', "Only english is supported for now"
        self.cache = cache
        self.lang = lang

    def labels_id_gen_(self):
        tree = load_xml("http://publications.europa.eu/resource/dataset/eurovoc", self.cache)
        for node in tree.findall(".//xs:enumeration", {'xs': "http://www.w3.org/2001/XMLSchema"}):
            doc = node.find('./xs:annotation/xs:documentation', {'xs': "http://www.w3.org/2001/XMLSchema"})
            if doc is not None:
                try:
                    label = doc.text.split('/')[0].strip()
                    identifier = node.attrib['value'].replace('eurovoc:', '')
                    yield identifier, label
                except Exception as e:
                    print(e)
                    import IPython; IPython.embed()
                    break

    @property
    def labels(self):
        return dict(self.labels_id_gen_())

    @property
    def identifers(self):
        return {v: k for k, v in self.labels_id_gen_()}
