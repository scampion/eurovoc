# EuroVoc

This package provides a simple interface to the EuroVoc thesaurus.

http://publications.europa.eu/resource/dataset/eurovoc

```python
import eurovoc
eurovoc.thesaurus_en_labels
```

will return a dictionary of EuroVoc labels in English.


```python 
import eurovoc

eurovoc.en_labels
eurovoc.en_identifiers

```

Will return a dictionnary and the reverse with term and id like :

```
'1892': 'meteorology',
'1893': 'methanol',
'1894': 'research method',
'1895': 'statistical method',
'1896': 'metrology',
```

⚠️ identifier  are not always number

