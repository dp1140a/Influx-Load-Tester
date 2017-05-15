#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import json
import random
import string
import sys
import getopt
from config import DEFAULT_CONFIG


class DataGenerator:
    def __init__(self, configFile):
        self.measurements = []
        self.tagKeySet = []
        self.fieldKeySet = []

        with open(configFile, "r") as fin:
            FILE_CONFIG = json.load(fin)

        self.config = DEFAULT_CONFIG.copy()
        self.config.update(FILE_CONFIG)
        print("CONFIG:\n" + json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))

        fieldTypeWeights = self.config.get("fieldTypeWeights")
        self.FIELD_TYPES = ["string"] * fieldTypeWeights[0].get("string") + \
                           ["int"] * fieldTypeWeights[1].get("int") + \
                           ["float"] * fieldTypeWeights[2].get("float") + \
                           ["boolean"] * fieldTypeWeights[3].get("boolean")

    # Generate a word of length random characters
    @staticmethod
    def randomWord(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    def randomInt(self):
        return random.randint(0, self.config.get("maxFieldNumericValue"))

    def randomDecimal(self):
        return self.randomInt() / pow(10, self.config.get("maxDecimalValueLength"))

    def setupMeasurements(self):
        if self.config["measurements"]:
            print("Manually defined measurements")
            for measurement in self.config["measurements"]:
                self.measurements.append(measurement)
        else:
            for num in range(self.config.get('numMeasurements')):
                self.measurements.append(self.randomWord(self.config.get('maxTagValueLength')))

        print('Measurements: ' + ', '.join(self.measurements))

    def setupTagKeys(self):
        if self.config["tags"]:
            print("Manually defined tags")
            for tag in self.config["tags"]:
                self.tagKeySet.append(tag)
        else:
            if self.config.get('minTags') > self.config.get('maxTags'):
                sys.exit('Error: minTags cannot be larger than maxTags.  Exiting!')
            else:
                for num in range(self.config.get('minTags'), self.config.get('maxTags') + 1):
                    self.tagKeySet.append(self.randomWord(self.config.get('maxTagValueLength')))

        print('Tag Key Set: ' + ', '.join(self.tagKeySet))

    def setupFieldKeys(self):
        if self.config["fields"]:
            print("Manually defined fields")
            for field in self.config["fields"]:
                self.fieldKeySet.append(field)
        else:
            if self.config.get('minFields') > self.config.get('maxFields'):
                sys.exit('Error: minFields cannot be larger than maxFields.  Exiting!')
            else:
                for num in range(self.config.get('minFields'), self.config.get('maxFields') + 1):
                    field = {"name": self.randomWord(self.config.get('maxFieldStrValueLength')),
                             "type": random.choice(self.FIELD_TYPES)}
                    self.fieldKeySet.append(field)

        print('Field Key Set:')
        print(json.dumps(self.fieldKeySet, sort_keys=True, indent=4, separators=(',', ': ')))

    def getBatch(self):
        batchSize = random.randint(self.config.get("minBatchSize"), self.config.get("maxBatchSize"))
        batch = []
        i = 0
        while i < batchSize:
            line = random.choice(self.measurements) + ","
            tagSet = []
            for tag in self.tagKeySet:
                tagSet.append(tag + "=" + self.randomWord(self.config.get('maxTagValueLength')))

            fieldSet = []
            for field in self.fieldKeySet:
                if field.get("type") == "string":
                    field = field.get("name") + "=\"" + self.randomWord(self.config.get('maxFieldStrValueLength')) + "\""
                elif field.get("type") == "int":
                    field = field.get("name") + "=" + str(self.randomInt())
                elif field.get("type") == "float":
                    field = field.get("name") + "=" + str(self.randomDecimal())
                elif field.get("type") == "boolean":
                    field = field.get("name") + "=" + str(bool(random.getrandbits(1))).lower()

                fieldSet.append(field)

            line += ','.join(tagSet) + " " + ','.join(fieldSet)
            #print(line)
            batch.append(line)
            i += 1
        return batch

    def writeBatchFile(self, batch):
        f = open(self.config.get("filename"), 'w')
        f.write("\n".join(batch))


if __name__ == '__main__':
    config = ""
    print(sys.argv)
    try:
        if len(sys.argv) > 1:
            opts, args = getopt.getopt(sys.argv[1:], "c:", ["config="])
        else:
            print("Usage: DataGenerator.py -c <configFile>")
            sys.exit()

    except getopt.GetoptError:
        print("Usage: DataGenerator.py -c <configFile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: DataGenerator.py -c <configFile>")
            sys.exit()
        elif opt in ("-c", "--config"):
            config = arg

    DG = DataGenerator(config)
    DG.setupMeasurements()
    DG.setupTagKeys()
    DG.setupFieldKeys()
    DG.writeBatchFile(DG.getBatch())
