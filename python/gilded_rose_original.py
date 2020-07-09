# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items # items is a list if Item objects

    def update_quality(self):
        for item in self.items: # looping through to update each item in items
            # "normal" items - items that lose quality
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert": # checks for 2 of 3 special items
                if item.quality > 0: # checks to ensure item is not below 0 quality (the min acceptable value)
                    if item.name != "Sulfuras, Hand of Ragnaros": # again checks for the final special item which value never changes
                        item.quality = item.quality - 1 # finally decrements item quality by 1
            # items that gain value (brie, backstage)
            else: # only brie, passes, and sulfuras will make it to this condition
                if item.quality < 50: # eliminates sulfuras (80 qual) leaving brie and backstage passes
                    item.quality = item.quality + 1 # increments quality by 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert": # special handling for passes
                        if item.sell_in < 11: # if within 10 days of sell-by, continue
                            if item.quality < 50: # cannot exceed 50 quality
                                item.quality = item.quality + 1 # increment quality 1, making a total of 2 increments for <10day pass
                        if item.sell_in < 6: # checks if pass is withing 5 days of sell-by
                            if item.quality < 50: # cannot exceed 50 quality
                                item.quality = item.quality + 1 # increment quality 1, making a total of 3 increments for <5day pass

            # decremend days to sale (note: update sell_in should not be in the update_quality?)
            if item.name != "Sulfuras, Hand of Ragnaros": # sulfuras has no sell-by date, thus we do not decrement
                item.sell_in = item.sell_in - 1 # if not sulfuras, simply decrement sell_in by 1

            # section to further decrease quality of past sell_in date
            if item.sell_in < 0: # checks if an item is past its sell-by date
                if item.name != "Aged Brie": # skips brie for handling of other items
                    if item.name != "Backstage passes to a TAFKAL80ETC concert": # skips passes for special handling
                        if item.quality > 0: # validates that quality must be non-negative
                            if item.name != "Sulfuras, Hand of Ragnaros": # skips sulfuras, as its quality never changes
                                item.quality = item.quality - 1 # further reduce quality by 1 if past sell-by, for total of 2
                    else: # if a backstage pass, set to 0
                        item.quality = 0 # deducts self from self to give 0
                else: # for brie value will go up double after sell_in date
                    if item.quality < 50: # items do not go over 50 value
                        item.quality = item.quality + 1 # increase value of brie again, for total of 2 if after sell-by


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
