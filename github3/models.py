# -*- coding: utf-8 -*-

"""
github3.models
~~~~~~~~~~~~~~

This module contains the models that comprise the Github API.
"""

import json
from urllib import quote

import requests
from .helpers import to_python
from .structures import *


class BaseResource(object):

    _strs = []
    _ints = []
    _dates = []
    _bools = []
    _dicts = []
    _map = {}
    _pks = []

    def __init__(self):
        self._bootstrap()
        self._h = None
        super(BaseResource, self).__init__()

    def __repr__(self):
        return "<resource '{0}'>".format(self._id)

    def _bootstrap(self):
        """Bootstraps the model object based on configured values."""

        for attr in self._keys():
            setattr(self, attr, None)

    def _keys(self):
        return self._strs + self._ints + self._dates + self._bools + self._map.keys()

    @property
    def _id(self):
        try:
            return getattr(self, self._pks[0])
        except IndexError:
            return None

    @property
    def _ids(self):
        """The list of primary keys to validate against."""
        for pk in self._pks:
            yield getattr(self, pk)

        for pk in self._pks:

            try:
                yield str(getattr(self, pk))
            except ValueError:
                pass


    def dict(self):
        d = dict()
        for k in self.keys():
            d[k] = self.__dict__.get(k)

        return d

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):

        d = to_python(
            obj=cls(),
            in_dict=d,
            str_keys=cls._strs,
            int_keys=cls._ints,
            date_keys=cls._dates,
            bool_keys=cls._bools,
            dict_keys= cls._dicts,
            object_map=cls._map,
            _h = h
        )

        d.__dict__.update(kwargs)

        return d


class Authorization(BaseResource):
    """Github Authorization."""

    _strs = ['url', 'scopes', 'token', 'note', 'note_url']
    _ints = ['id']
    _dates = ['created_at', 'updated_at']
    _pks = ['id']

    def __repr__(self):
        return "<authorization '{0}'>".format(self.id)

    def new(self, scopes=None, note=None, note_url=None):
        """Creates a new authorization."""

        payload = {}

        if scopes:
            payload['scopes'] = scopes

        if note:
            payload['note'] = note
        
        if note_url:
            payload['note_url'] = note_url

        r = self._h._http_resource(
            method='POST',
            resource=('authorizations',),
            data=payload
        )

        _id = json.loads(r.content).get('id')
        return self._h.authorizations.get(_id)
        return r.ok

    def destroy(self):
        """Destoys the app. Do be careful."""

        r = self._h._http_resource(
            method='DELETE',
            resource=('authorizations', self.id)
        )
        return r.ok

