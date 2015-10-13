from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from nose.tools import (assert_true,
                        assert_equal)
import unittest

import datapackage_registry

import httpretty

BACKEND_URL = "https://rawgit.com/dataprotocols/registry/master/registry.csv"


class DataPackageRegistryGetTest(unittest.TestCase):

    '''Tests for registry.get()'''

    @httpretty.activate
    def test_return_empty_array_when_registry_is_empty(self):
        '''Return an empty array when registry csv is empty'''
        httpretty.register_uri(httpretty.GET, BACKEND_URL,
                               body="id,title,schema,specification")

        assert_equal(datapackage_registry.get(), [],
                     'Registry is not an empty array')

    @httpretty.activate
    def test_return_non_empty_array_when_registry_is_not_empty(self):
        '''Return an array of dicts when registry csv is not empty'''

        body = """id,title,schema,specification
base,Data Package,https://example.com/one.json,http://example.com
tabular,Tabular Data Package,https://example.com/two.json,http://example.com"""

        httpretty.register_uri(httpretty.GET, BACKEND_URL, body=body)

        reg = datapackage_registry.get()
        assert_equal(len(reg), 2)
        # each member in array is a dict
        for o in reg:
            assert_equal(type(o), dict)

    @httpretty.activate
    def test_dicts_have_expected_keys(self):
        '''The returned dicts have the expected keys'''

        body = """id,title,schema,specification
base,Data Package,https://example.com/one.json,http://example.com
tabular,Tabular Data Package,https://example.com/two.json,http://example.com"""

        httpretty.register_uri(httpretty.GET, BACKEND_URL, body=body)

        reg = datapackage_registry.get()

        # each dict in array has the expected keys
        for o in reg:
            assert_true('id' in o)
            assert_true('title' in o)
            assert_true('schema' in o)
            assert_true('specification' in o)

    @httpretty.activate
    def test_dicts_have_expected_values(self):
        '''The returned dicts have the expected values'''

        body = """id,title,schema,specification
base,Data Package,https://example.com/one.json,http://example.com
tabular,Tabular Data Package,https://example.com/two.json,http://example.com"""

        httpretty.register_uri(httpretty.GET, BACKEND_URL, body=body)

        reg = datapackage_registry.get()

        # first dict in array has the expected values
        assert_equal(reg[0]['id'], 'base')
        assert_equal(reg[0]['title'], 'Data Package')
        assert_equal(reg[0]['schema'], 'https://example.com/one.json')
        assert_equal(reg[0]['specification'], 'http://example.com')
