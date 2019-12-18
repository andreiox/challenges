import json
import random
import sys

from lxml import etree


folder = 'schemas/'
namespaces = { 'xs': 'http://www.w3.org/2001/XMLSchema' }

simpletypes = {}
complextypes = {}

def generate_fake_values_element(filename, element_name = None):
    tree = etree.parse(filename)

    includes = tree.xpath('//xs:include', namespaces = namespaces)
    for schema in includes:
        generate_fake_values_element(f'{folder}{schema.get("schemaLocation")}')

    load_simpletypes(tree)
    load_complextypes(tree)

    if element_name:
        element = list(filter(lambda e: e.get('name') == element_name, tree.xpath('xs:element', namespaces = namespaces)))[0]
        return { element_name: generate_fake_values(element.get('type')) }

def load_simpletypes(tree):
    types = tree.xpath('xs:simpleType', namespaces = namespaces)
    for ttype in types:
        name = ttype.get('name')
        base = ttype.xpath('xs:restriction', namespaces = namespaces)[0].get('base')

        simpletypes[name] = base

def load_complextypes(tree):
    types = tree.xpath('//xs:complexType', namespaces = namespaces)
    for ttype in types:
        name = get_complextype_name_or_random(ttype)

        elements = map(extract_name_type, ttype.xpath('xs:sequence/xs:element', namespaces = namespaces))
        attributes = map(extract_name_type, ttype.xpath('xs:attribute', namespaces = namespaces))

        if len(list(filter(lambda e: e.tag.endswith('simpleContent'), ttype.getchildren()))) != 0:
            attributes = map(extract_name_type, ttype.xpath('xs:simpleContent/xs:extension/xs:attribute', namespaces = namespaces))
            elements = [{ 'name': '$value', 'type': 'string' }]

        complextypes[name] = { 'elements': elements, 'attributes': attributes }

def get_complextype_name_or_random(ttype):
    name = ttype.get('name')
    if not name:
        ttype.set('name', str(random.random()))
        name = ttype.get('name')

    parent = ttype.getparent()
    if not parent.get('type'):
        parent.set('type', name)

    return name

def extract_name_type(node):
    ttype = node.get('type')
    if not ttype:
        if len(list(filter(lambda e: e.tag.endswith('complexType'), node.getchildren()))) != 0:
            ttype = node.xpath('xs:complexType', namespaces = namespaces)[0].get('name')
        elif len(list(filter(lambda e: e.tag.endswith('simpleType'), node.getchildren()))) != 0:
            ttype = node.xpath('xs:simpleType/xs:restriction', namespaces = namespaces)[0].get('base')

    return { 'name': node.get('name'), 'type': ttype }

def generate_fake_values(ttype):
    if ttype in complextypes:
        structure = {}
        complextype = complextypes[ttype]

        attributes = list(complextype['attributes'])
        if len(attributes):
            structure['attributes'] = {}
            for attr in attributes:
                structure['attributes'][attr['name']] = generate_fake_values(attr['type'])

        elements = list(complextype['elements'])
        for element in elements:
            structure[element['name']] = generate_fake_values(element['type'])

        return structure

    return 'string'

fake_element = generate_fake_values_element(sys.argv[1], sys.argv[2])
print(json.dumps(fake_element, indent=4))
