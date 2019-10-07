from os import listdir
from os.path import isfile, join
from pathlib import Path
import importlib

import sys 
sys.path.append('../')
from back.core.AppModel import AppModel

blocksDir = "DBuilder"
blocksPath = Path().parent.joinpath(blocksDir).absolute()

class DBuilder(AppModel):
    buildBlocks = []

    def __init__(self):
        super().__init__()
        self.run()

    def getBlocks(self):
        self.buildBlocks = [f.replace(".py", "") for f in listdir(blocksPath) if isfile(join(blocksPath, f))]

    def  getBlockType(self, block):
        return block.split("-")[1]
    
    def  getBlockName(self, block):
        return block.split("-")[0]

    def putBlock(self, block, fields):
        res = self.dbDriver.query("CREATE TABLE IF NOT EXISTS " + str(block), fields)
        if res :
            print(str(block) + " CREADO")
        else:
            print(str(block) + " ERROR")


    def run(self):

        self.getBlocks()
        for block in self.buildBlocks:

            blockType = self.getBlockType(block)
            blockName = self.getBlockName(block)

            cls = getattr(importlib.import_module('DBuilder.' + block), blockName)
            if blockType == 'table':
                self.putBlock(blockName, cls.fields)
            