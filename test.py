import unittest
import pyautogui
import re
import os
import json
import sys
from time import sleep
import typing
from subprocess import Popen

import defaults.tkhelper as Helper

class RegexTests(unittest.TestCase):

    def test_builtin_func(self):
        pattern = re.compile(Helper.Default.builtin_pattern_detailed)
        textToTest = ' abs delattr hash memoryview set all dict help min setattr any dir hex next slice ascii divmod id object sorted bin enumerate input oct staticmethod bool eval int open str breakpoint isinstance ord sum bytearray filter issubclass pow super bytes float iter print tuple callable format len property type chr frozenset list range vars classmethod getattr locals repr zip compile globals map reversed __import__ complex hasattr max round aabsa delattra hasha memoryviewa seta alla dicta helpa mina setattra anya dira hexa nexta slicea asciia divmoda ida objecta sorteda bina enumeratea inputa octa staticmethoda boola evala inta opena stra breakpointa isinstancea orda suma bytearraya filtera issubclassa powa supera bytesa floata itera printa tuplea callablea formata lena propertya typea chra frozenseta lista rangea varsa classmethoda getattra localsa repra zipa compilea globalsa mapa reverseda __import__a complexa hasattra maxa roundabs adelattr ahash amemoryview aset aall adict ahelp amin asetattr aany adir ahex anext aslice aascii adivmod aid aobject asorted abin aenumerate ainput aoct astaticmethod abool aeval aint aopen astr abreakpoint aisinstance aord asum abytearray afilter aissubclass apow asuper abytes afloat aiter aprint atuple acallable aformat alen aproperty atype achr afrozenset alist arange avars aclassmethod agetattr alocals arepr azip acompile aglobals amap areversed a__import__ acomplex ahasattr amax arounda '

        matches = re.findall(pattern, textToTest)
        self.assertEqual(len(matches), 68)

    def test_strings(self):
        pattern = re.compile(Helper.Default.strings_pattern)
        textToTest = "abc a gdsa'fdsa'dfsa dfsa\"afsd\"afsd"

        matches = re.findall(pattern, textToTest)
        self.assertEqual(len(matches), 2)

    def test_chain_pattern_detailed(self):
        pattern = re.compile(Helper.Default.chain_pattern_detailed)
        textToTest = ' False class finally is return None continue for lambda try True def from nonlocal while and del global not with as elif if or yield assert else import pass break except in raise aFalse aclass afinally ais areturn aNone acontinue afor alambda atry aTrue adef afrom anonlocal awhile aand adel aglobal anot awith aas aelif aif aor ayield aassert aelse aimport apass abreak aexcept ain araise Falsea classa finallya isa returna Nonea continuea fora lambdaa trya Truea defa froma nonlocala whilea anda dela globala nota witha asa elifa ifa ora yielda asserta elsea importa passa breaka excepta ina raisea false '

        matches = re.findall(pattern, textToTest)
        self.assertEqual(len(matches), 33)

    def test_digits_pattern(self):
        pattern = re.compile(Helper.Default.digits_pattern)
        textToTest = "12.231 12 123a a4121 231.213.132"
        
        matches = re.findall(pattern, textToTest)
        self.assertEqual(len(matches), 2)


class GuiTests(unittest.TestCase):
    screenShotsDirectory = os.path.join(os.getcwd(), 'gui-screens')
    fileToWriteTo = os.path.join(os.getenv('HOME'), 'file.txt') # to avoid unnecessary clicking, file dialog default opens home directory
    # remember not to change default dir in config.json file to other than /home/$USER

    screenWidth, screenHeight = pyautogui.size() # written for 1280x1024

    if screenWidth < 1280 or screenHeight < 1024:
        print('Your resolution is too low, 1280x1024 is minimum!')
        sys.exit(1)

    fileMenu = (18, 48)
    exitMenuButton = (35, 180)
    openFileMenuButton = (39, 99)
    fileNameEntry = (548, 645)
    openFileButton = (800, 645)
    openedFileTab = (187, 81)
    textEntryField = (77, 189)
    saveFileMenuButton = (48, 121)
    saveFileButton = (799, 649)

    @classmethod
    def setUpClass(cls): # set up the config json file and edit it
        p = Popen(('python3', 'main_frame.py'))
        p.kill()
        configDict = json.load(open(os.path.join(os.getenv('HOME'), '.config/PyEnlightenmentCode/.config.json')))
        configDict['x'] = 1280
        configDict['y'] = 931
        configDict['wind_y'] = 0
        configDict['wind_x'] = 0
        json.dump(configDict, open(os.path.join(os.getenv('HOME'), '.config/PyEnlightenmentCode/.config.json'), 'w'))
    
    def setUp(self):
        with open(GuiTests.fileToWriteTo, 'w+') as f:
            f.write("This is a test text file")
        Popen(('python3.7', 'main_frame.py', "-q"))
        sleep(3)
    
    def test_fileLoad(self):
        pyautogui.moveTo(GuiTests.fileMenu)
        pyautogui.click()

        pyautogui.moveTo(GuiTests.openFileMenuButton)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.fileNameEntry)
        pyautogui.click()
        pyautogui.write('file.txt', interval=0.1)
        pyautogui.moveTo(GuiTests.openFileButton)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.openedFileTab)
        pyautogui.click()

        try:
            location = pyautogui.locateOnScreen(os.path.join(GuiTests.screenShotsDirectory, 'loadFileEffect.png'))
        except:
            self.assertEqual(0, 1)
        finally:
            self.assertNotEqual(location, None)

    def test_fileWrite(self):
        pyautogui.moveTo(GuiTests.textEntryField)
        pyautogui.click()

        pyautogui.write('this is a write test', interval=0.1)
        pyautogui.moveTo(GuiTests.fileMenu)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.saveFileMenuButton)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.fileNameEntry)
        pyautogui.click()
        pyautogui.write('write.txt', interval=0.1)
        pyautogui.moveTo(GuiTests.saveFileButton)
        pyautogui.click()

        with open(os.path.join(os.getenv('HOME'), 'write.txt')) as f:
            text = f.readlines()[0]
            print(text)
            self.assertEqual(text, 'this is a write test\n')

        os.remove(os.path.join(os.getenv('HOME'), 'write.txt'))
        
    def test_fileOverwrite(self):
        pyautogui.moveTo(GuiTests.textEntryField)
        pyautogui.click()

        pyautogui.write('this is an overwrite test', interval=0.1)
        pyautogui.moveTo(GuiTests.fileMenu)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.saveFileMenuButton)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.fileNameEntry)
        pyautogui.click()
        pyautogui.write('file.txt', interval=0.1)
        pyautogui.moveTo(GuiTests.saveFileButton)
        pyautogui.click()
        pyautogui.press('enter')

        with open(os.path.join(os.getenv('HOME'), 'file.txt')) as f:
            text = f.readlines()[0]
            print(text)
            self.assertEqual(text, 'this is an overwrite test\n')

    def tearDown(self):
        pyautogui.moveTo(GuiTests.fileMenu)
        pyautogui.click()
        pyautogui.moveTo(GuiTests.exitMenuButton)
        pyautogui.click()
        os.remove(GuiTests.fileToWriteTo)
        configDict = json.load(open(os.path.join(os.getenv('HOME'), '.config/PyEnlightenmentCode/.config.json')))
        configDict['x'] = 1280
        configDict['y'] = 931
        configDict['wind_y'] = 0
        configDict['wind_x'] = 0
        json.dump(configDict, open(os.path.join(os.getenv('HOME'), '.config/PyEnlightenmentCode/.config.json'), 'w'))

if __name__ == "__main__":
    unittest.main()
