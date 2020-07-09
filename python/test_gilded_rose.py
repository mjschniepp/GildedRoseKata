# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    '''
        Original Test Cases
    '''
    def test_normal(self):
        items = [Item("normal1", 1, 10),
                 Item("normalMax", 0, 50),
                 Item("normalMin", -1, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[1].sell_in, -1)
        self.assertEqual(items[2].sell_in, -2)
        self.assertEqual(items[0].quality, 9)
        self.assertEqual(items[1].quality, 48)
        self.assertEqual(items[2].quality, 0)

    def test_conjured(self):
        items = [Item("Conjured Mana Cake", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].name, "Conjured Mana Cake")

    def test_sulfuras(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 80)

    def test_brie(self):
        items = [Item("Aged Brie", 1, 2),
                 Item("Aged Brie", 0, 2),
                 Item("Aged Brie", -1, 2)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 3)
        self.assertEqual(items[1].quality, 4)
        self.assertEqual(items[2].quality, 4)

    def test_backstage(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 10),
                 Item("Backstage passes to a TAFKAL80ETC concert", 9, 10),
                 Item("Backstage passes to a TAFKAL80ETC concert", 4, 10),
                 Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 14)
        self.assertEqual(items[0].quality, 11)
        self.assertEqual(items[1].quality, 12)
        self.assertEqual(items[2].quality, 13)
        self.assertEqual(items[3].quality, 0)

    '''
        Additional Test Cases Added During Refactor
    '''
    def test_update_normal(self):
        items = [Item("normal 1", 10, 10),
                 Item("normal 2", 0, 1),
                 Item("normal 3", -1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 9)
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[1].quality, 0)
        self.assertEqual(items[1].sell_in, -1)
        self.assertEqual(items[2].quality, 0)
        self.assertEqual(items[2].sell_in, -2)

    def test_update_conjured(self):
        items = [Item("conjured 1", 10, 10),
                 Item("conjured 2", 0, 1),
                 Item("conjured 3", -1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 8)
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[1].quality, 0)
        self.assertEqual(items[1].sell_in, -1)
        self.assertEqual(items[2].quality, 0)
        self.assertEqual(items[2].sell_in, -2)

    def test_update_brie(self):
        items = [Item("Aged Brie 1", 1, 1),
                 Item("Aged Brie 2", 0, 50),
                 Item("Aged Brie 3", -1, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 2)
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[1].quality, 50)
        self.assertEqual(items[1].sell_in, -1)
        self.assertEqual(items[2].quality, 50)
        self.assertEqual(items[2].sell_in, -2)

    def test_update_backstage(self):
        items = [Item("backstage 1", 11, 5),
                 Item("backstage 2", 10, 6),
                 Item("backstage 3", 6, 14),
                 Item("backstage 4", 5, 16),
                 Item("backstage 5", 1, 28),
                 Item("backstage 6", 0, 31),
                 Item("backstage 7", -3, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 6)
        self.assertEqual(items[0].sell_in, 10)
        self.assertEqual(items[1].quality, 8)
        self.assertEqual(items[1].sell_in, 9)
        self.assertEqual(items[2].quality, 16)
        self.assertEqual(items[2].sell_in, 5)
        self.assertEqual(items[3].quality, 19)
        self.assertEqual(items[3].sell_in, 4)
        self.assertEqual(items[4].quality, 31)
        self.assertEqual(items[4].sell_in, 0)
        self.assertEqual(items[5].quality, 0)
        self.assertEqual(items[5].sell_in, -1)
        self.assertEqual(items[6].quality, 0)
        self.assertEqual(items[6].sell_in, -4)

    def test_update_sulfuras(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 1, 80),
                 Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 80)
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[1].quality, 80)
        self.assertEqual(items[1].sell_in, -1)

if __name__ == '__main__':
    unittest.main()
