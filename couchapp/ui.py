# -*- coding: utf-8 -*-
#
# Copyright 2008,2009  Benoit Chesneau <benoitc@e-engura.org>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at#
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import codecs
import copy
from hashlib import md5
import httplib
import logging
import os
import shutil
import socket
import string
import sys
import time
import urllib

try:
    import json
except ImportError:
    import simplejson as json


from couchapp import __version__
from couchapp.extensions import GLOBAL_EXTENSIONS
from couchapp.http import create_db
from couchapp.errors import AppError
from couchapp.utils import *
from couchapp.vendor import Vendor

USER_AGENT = 'couchapp/%s' % __version__

class NullHandler(logging.Handler):
    """ null log handler """
    def emit(self, record):
        pass


class UI(object):
    
    DEFAULT_SERVER_URI = 'http://127.0.0.1:5984/'
    
    def __init__(self, verbose=1, logging_handler=None):
        # load user conf
        self.conf = {}
        # init extensions
        self.conf['extensions'] = GLOBAL_EXTENSIONS
        self.verbose = verbose
        self.readconfig(rcpath())
        # init logger
        if logging_handler is None:
            logging_handler = NullHandler()
        self.logger = logging.getLogger("couchapp")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging_handler)
        
    def set_verbose(self, level):
        self.verbose = level
        
    def readconfig(self, fn):
        """ Get current configuration of couchapp.
        """
        conf = self.conf or {}
        if isinstance(fn, basestring):
            fn = [fn]
        
        for f in fn:
            if os.path.isfile(f):
                conf.update(self.read_json(f, use_environment=True))
        self.conf = conf

    def updateconfig(self, app_dir):
        conf_files = [os.path.join(app_dir, 'couchapp.json'),
            os.path.join(app_dir, '.couchapprc')]
        self.readconfig(conf_files)
        
                        
    def split_path(self, path):
        parts = []
        while True:
            head, tail = os.path.split(path)
            parts = [tail] + parts
            path = head
            if not path: break
        return parts
        
    def deltree(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.unlink(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        try:
            os.rmdir(path)
        except:
            pass
                
    def execute(cmd):
        return popen3(cmd)
        
    def sign(self, fpath):
        """ return md5 hash from file content

        :attr fpath: string, path of file

        :return: string, md5 hexdigest
        """
        if os.path.isfile(fpath):
            m = md5()
            fp = open(fpath, 'rb')
            try:
                while 1:
                    data = fp.read(8096)
                    if not data: break
                    m.update(data)
            except IOError, msg:
                sys.stderr.write('%s: I/O error: %s\n' % (fpath, msg))
                return 1
            fp.close()
            return m.hexdigest()
        return ''
        
    def read(self, fname, utf8=True, force_read=False):
        """ read file content"""
        if utf8:
            try:
                f = codecs.open(fname, 'rb', "utf-8")
                data = f.read()
                f.close()
            except UnicodeError, e:
                if force_read:
                    return self.read(fname, utf8=False)
                raise
        else:
            f = open(fname, 'rb')
            data = f.read()
            f.close()
            
        return data
               
    def write(self, fname, content):
        """ write content in a file

        :attr fname: string,filename
        :attr content: string
        """
        f = open(fname, 'wb')
        f.write(to_bytestring(content))
        f.close()

    def write_json(self, fname, content):
        """ serialize content in json and save it

        :attr fname: string
        :attr content: string

        """
        self.write(fname, json.dumps(content).encode('utf-8'))

    def read_json(self, fname, use_environment=False):
        """ read a json file and deserialize

        :attr filename: string
        :attr use_environment: boolean, default is False. If
        True, replace environment variable by their value in file
        content

        :return: dict or list
        """
        try:
            data = self.read(fname, force_read=True)
        except IOError, e:
            if e[0] == 2:
                return {}
            raise

        if use_environment:
            data = string.Template(data).substitute(os.environ)

        try:
            data = json.loads(data)
        except:
            if self.verbose >= 1:
                self.logger.error("Json is invalid, can't load %s" % fname)
            return {}
        return data
       
    def get_dbs(self, dbstring=None):
        if dbstring is None or not "/" in dbstring:
            env = self.conf.get('env', {})
            if dbstring is not None:
                db_env = "%s%s" % (self.DEFAULT_SERVER_URI, dbstring)
                if dbstring in env:
                    db_env = env[dbstring].get('db', db_env)
            else: 
                if 'default' in env:
                    db_env = env['default']['db']
                else:
                    raise AppError("database isn't specified")

            if isinstance(db_env, basestring):
                self.db_url = [db_env]
            else:
                self.db_url = db_env
        else:
            self.db_url = [dbstring]
          
        for i, db in enumerate(self.db_url):
            try:
                create_db(db)
            except:
                pass    
        return self.db_url

    def get_app_name(self, dbstring, default):
        env = self.conf.get('env', {})
        if dbstring and not "/" in dbstring:
            if dbstring in env:
                return env[dbstring].get('name', default)
            elif  'default' in env:
                return env['default'].get('name', default)
        elif not dbstring:
            if 'default' in env:
                return env['default'].get('name', default)
        return default