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
        self.resourceManager = ResourceManager()
        FileTagger.instance = self

    def setTagToFile(self, path, tag, add=True):
        fileRes = self.getResource(path)
        if fileRes:
            fileRes.setTag(tag, add)
            fileRes.save()

    def setTagToDir(self, path, tag, add=True):
        tagger = self.taggerManager.registerTagger(path)
        tagger.setDirTag(tag, add)
        tagger.save()

    def search(self, tags, mode="and", path=None):
        results = []
        self.taggerManager.scanTaggers(path)
        for tagger in self.taggerManager.getTaggers():
            results.extend(tagger.search(tags, mode))
        return results

    def getResource(self, path):
        path = os.path.abspath(path)
        if os.path.isfile(path):
            dirname, filename = os.path.split(path)
            tagger = self.taggerManager.registerTagger(dirname)
            fileRes = self.resourceManager.registerResource(path, tagger)
            return fileRes

    def getInstance():
        return FileTagger.instance if FileTagger.instance else FileTagger()


class TaggerManager(object):

    """Tagger Manager"""

    defaultConfig = ".fileTagger"

    def __init__(self):
        super(TaggerManager, self).__init__()
        self.__taggers = []
        self.__indexBox = {}

    def scanTaggers(self, path=None):
        count = 0
        path = path if path else os.path.abspath("")
        for currentDir, dirname, filename in os.walk(path):
            if TaggerManager.defaultConfig in filename:
                taggerPath = os.path.join(
                    currentDir, TaggerManager.defaultConfig)
                self.registerTagger(taggerPath)
                count = count + 1
        return count

    def addTagger(self, filename):
        filename = os.path.normpath(filename)
        tagger = Tagger(filename)
        self.__taggers.append(tagger)
        self.__indexBox[filename] = tagger
        return tagger

    def registerTagger(self, path):
        if os.path.isdir(path):
            path = os.path.join(path, TaggerManager.defaultConfig)
        path = os.path.normpath(path)
        if path in self.__indexBox:
            return self.__indexBox[path]
        else:
            return self.addTagger(path)

    def getTaggers(self):
        return self.__taggers.copy()


class Tagger(object):

    """Tag Class"""

    def __init__(self, filename=None):
        super(Tagger, self).__init__()
        config = configparser.ConfigParser()
        if filename:
            self.__configPath = filename
            if os.path.isfile(filename):
                config.read(filename)
        self.__fixConfig(config)
        self.__config = config
        self.__loadDirTags()

    def __fixConfig(self, config):
        if not config.has_section("Folder"):
            config.add_section("Folder")
        if not config.has_section("Tags"):
            config.add_section("Tags")
        # path = os.path.abspath(self.__configPath)
        # os.popen("attrib +h {path}".format(path=path))
        # if hide it, you need permission to edit the file

    def __loadDirTags(self):
        if self.__config.has_option("Folder", "Tags"):
            tags = self.__config.get("Folder", "Tags")
            self.__tags = TagManager.parse(tags)
        else:
            self.__tags = []

    def save(self, path=None):
        dirTags = TagManager.convert(self.__tags)
        self.__config.set("Folder", "Tags", dirTags)
        path = path if path else self.__configPath
        self.__config.write(open(path, "w"))

    def getTags(self, filename):
        filename = os.path.basename(filename)
        if self.__config.has_option("Tags", filename):
            return TagManager.parse(self.__config.get("Tags", filename))
        else:
            return []

    def setTags(self, filename, tags):
        filename = os.path.basename(filename)
        if isinstance(tags, (str)):
            self.__config.set("Tags", filename, tags)
        elif isinstance(tags, (list)):
            tagText = TagManager.convert(tags)
            # print(tagText)
            self.__config.set("Tags", filename, tagText)

    def setDirTag(self, tag, add=True):
        if add and tag not in self.__tags:
            self.__tags.append(tag)
        if not add and tag in self.__tags:
            self.__tags.remove(tag)

    def search(self, tags, mode="and"):
        if isinstance(tags, str):
            tags = [tags]
        results = []
        if mode == "and":
            if set(tags).issubset(set(self.__tags)):
                results.append(os.path.dirname(self.__configPath))
            for name in self.__config.options("Tags"):
                if set(tags).issubset(set(self.getTags(name))):
                    results.append(name)
        elif mode == "or":
            for tag in self.__tags:
                if tag in tags:
                    results.append(os.path.dirname(self.__configPath))
                    break
            for name in self.__config.options("Tags"):
                for tag in self.getTags(name):
                    if tag in tags:
                        results.append(name)
                        break
        path = os.path.dirname(self.__configPath)
        return [os.path.join(path, name) for name in results]


class ResourceManager(object):

    """To manage resources"""

    def __init__(self):
        super(ResourceManager, self).__init__()
        self.__resources = []
        self.__indexBox = {}

    def addResource(self, path, tagger):
        path = os.path.normpath(path)
        resource = Resource(path, tagger)

        self.__resources.append(resource)
        self.__indexBox[path] = resource
        return resource

    def registerResource(self, path, tagger=None):
        path = os.path.normpath(path)
        if path in self.__indexBox:
            return self.__indexBox[path]
        else:
            return self.addResource(path, tagger)


class Resource(object):

    """Resource(file or folder) for fileTagger"""

    def __init__(self, resPath, tagger):
        super(Resource, self).__init__()
        self.tagger = tagger
        self.path = resPath
        self.tags = tagger.getTags(resPath)

    def addTag(self, tag):
        self.setTag(tag)

    def removeTag(self, tag):
        self.setTag(tag, False)

    def setTag(self, tag, add=True):
        self.tags.append(tag) if add and not self.hasTag(tag) else False
        self.tags.remove(tag) if self.hasTag(tag) and not add else False

    def getTags(self):
        return self.tags.copy()

    def hasTag(self, tag):
        return True if tag in self.tags else False

    def save(self):
        self.tagger.setTags(self.path, self.tags)
        self.tagger.save()


class TagManager(object):

    """Class to manage tags"""

    def parse(text):
        return [tag for tag in filter(None, text.split(';'))]

    def convert(tags):
        return ';'.join(tags)
