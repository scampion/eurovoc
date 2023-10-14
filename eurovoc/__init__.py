import urllib
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
    xml = response.read()
    return ET.fromstring(xml)


def thesaurus_uris(cache=True):
    tree = load_xml("http://publications.europa.eu/resource/dataset/eurovoc", cache)
    return {r.attrib['thesaurus_id']: r.attrib['thesaurus_uri']
            for r in tree.findall(".//record[@thesaurus_id!='']")}


def thesaurus_en_labels(cache=True):
    def _thesaurus_en_labels():
        for k, v in thesaurus_uris(cache).items():
            tree = load_xml(v, cache)
            node = tree.find(".//dcterms:title[@xml:lang='en']",
                             {'dcterms': "http://purl.org/dc/terms/", "xml": "http://www.w3.org/XML/1998/namespace"})
            yield k, node.text.replace(k, '').strip()
    return dict(_thesaurus_en_labels())
