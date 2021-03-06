# fileTagger.py -- To add tags to files and manage files via tags
# @Zaeworks

''' File Tagger
    Copyright (C) 2015 Zaeworks

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import configparser
import os


class FileTagger(object):

    """Init of fileManager"""

    instance = None

    def __init__(self):
        super(FileTagger, self).__init__()
        self.taggerManager = TaggerManager()
        self.tagManager = TagManager()
        self.baseResourceManager = BaseResourceManager()
        FileTagger.instance = self

    def search(self, tags, mode="and"):
        results = []
        for tagger in self.taggerManager.getTaggers():
            results.extend(tagger.search(tags, mode))
        return results

    def getBaseResource(self, path, isFile=None, tagger=None):
        return self.baseResourceManager.registerResource(path, isFile, tagger)

    def getInstance():
        return FileTagger.instance if FileTagger.instance else FileTagger()


class TaggerManager(object):

    """Tagger Manager"""

    defaultConfig = ".fileTagger"

    def __init__(self):
        super(TaggerManager, self).__init__()
        self.taggers = []
        self.indexBox = {}

    def addTagger(self, filename):
        filename = os.path.normpath(filename)
        tagger = Tagger(filename)
        self.taggers.append(tagger)
        self.indexBox[filename] = tagger
        return tagger

    def registerTagger(self, path):
        if os.path.isdir(path):
            path = os.path.join(path, TaggerManager.defaultConfig)
        path = os.path.normpath(path)
        if path in self.indexBox:
            return self.indexBox[path]
        else:
            return self.addTagger(path)

    def getTaggers(self):
        return self.taggers.copy()


class Tagger(object):

    """Tag Class"""

    def __init__(self, filename=None):
        super(Tagger, self).__init__()
        config = configparser.ConfigParser()
        self.config = config
        if filename:
            self.configPath = filename
            if os.path.isfile(filename):
                config.read(filename)
        self.__fixConfig(config)
        self.__loadDirTags()

    def __fixConfig(self, config):
        if not config.has_section("Folder"):
            config.add_section("Folder")
        if not config.has_section("Tags"):
            config.add_section("Tags")
        # path = os.path.abspath(self.configPath)
        # os.popen("attrib +h {path}".format(path=path))
        # if hide it, you need permission to edit the file

    def __loadDirTags(self):
        if self.config.has_option("Folder", "Tags"):
            tags = self.config.get("Folder", "Tags")
            self.__tags = TagManager.parse(tags)
        else:
            self.__tags = []

    def save(self, path=None):
        dirTags = TagManager.convert(self.__tags)
        self.config.set("Folder", "Tags", dirTags)
        path = path if path else self.configPath
        self.config.write(open(path, "w"))
        if not self.__tags and not self.config.options("Tags"):
            os.remove(path)

    def getTags(self, filename):
        filename = os.path.basename(filename)
        if self.config.has_option("Tags", filename):
            return TagManager.parse(self.config.get("Tags", filename))
        else:
            return []

    def setTags(self, filename, tags):
        tagText = TagManager.convert(tags)
        if tagText:
            self.config.set("Tags", filename, tagText)
        elif self.config.has_option("Tags", filename):
            self.config.remove_option("Tags", filename)
        self.save()

    def setDirTag(self, tag, add=True):
        if add and tag not in self.__tags:
            self.__tags.append(tag)
        if not add and tag in self.__tags:
            self.__tags.remove(tag)

    def setDirTags(self, tags):
        self.__tags = tags.copy()
        self.save()

    def getDirTags(self):
        return self.__tags.copy()

    def search(self, keytags, mode='and'):
        keytags = [keytags] if isinstance(keytags, str) else keytags

        def matchAnd(tags): return set(keytags).issubset(set(tags))

        def matchOr(tags): return True in [tag in tags for tag in keytags]

        match = matchAnd if mode == 'and' else matchOr
        results, dirpath = [], os.path.dirname(self.configPath)
        match(self.__tags) and results.append(Folder(dirpath, self))
        for f in self.config.options("Tags"):
            if match(self.getTags(f)):
                results.append(File(os.path.join(dirpath, f), self))
        return results


class TagManager(object):

    """Class to manage tags"""

    def parse(text):
        return [tag for tag in filter(None, text.split(';'))]

    def convert(tags):
        return ';'.join(tags)


class BaseResourceManager(object):

    """New resource manager"""

    def __init__(self):
        self.resources = []
        self.indexBox = {}

    def addResource(self, path, isFile, tagger):
        resource = File(path, tagger) if isFile else Folder(path, tagger)
        self.resources.append(resource)
        self.indexBox[path] = resource
        return resource

    def registerResource(self, path, isFile=None, tagger=None):
        path = os.path.abspath(path)
        if path in self.indexBox:
            return self.indexBox[path]
        else:
            if isFile is None:
                isFile = os.path.isfile(path)
            return self.addResource(path, isFile, tagger)


class BaseResource(object):

    """Base file/folder resource class"""

    def __init__(self, path, isFile, tagger=None):
        self.path = os.path.abspath(path)
        self.basename = os.path.basename(path)
        self.isFile = isFile

        if not tagger:
            taggerPath = os.path.dirname(self.path) if isFile else self.path
            taggerManager = FileTagger.getInstance().taggerManager
            self.tagger = taggerManager.registerTagger(taggerPath)
        else:
            self.tagger = tagger

    def save(self):
        pass

    def setTag(self, tag, add=True):
        self.tags.append(tag) if add and not self.hasTag(tag) else False
        self.tags.remove(tag) if self.hasTag(tag) and not add else False

    def getTags(self):
        return self.tags.copy()

    def setTags(self, tags):
        self.tags = tags.copy()

    def hasTag(self, tag):
        return tag in self.tags


class File(BaseResource):

    """File resource class"""

    def __init__(self, path, tagger=None):
        super(File, self).__init__(path, True, tagger)
        self.tags = self.tagger.getTags(self.basename)

    def save(self):
        self.tagger.setTags(self.basename, self.tags)


class Folder(BaseResource):

    """Folder resource class"""

    def __init__(self, path, tagger=None):
        super(Folder, self).__init__(path, False, tagger)
        self.tags = self.tagger.getDirTags()

    def save(self):
        self.tagger.setDirTags(self.tags)
