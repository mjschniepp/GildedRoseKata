# Michael's Solution to the Gilded Rose

Here I will explain my strategy to complete the Gilded Rose kata along with some additional explanation of the code. While refactoring this piece of code there were four major components to my approach:

 - Understanding the "client" requirements
 - Understanding the existing code
 - Writing unit tests
 - Refactoring

 The first two steps listed came first and were done in sequence while the second also followed similarly but as the refactoring continued, many more unit tests were added and removed as needed.

 ## Understanding the Requirements

 Naturally, the first step in the procedure was to know what was being asked of me. The kata includes some instructions in the form of a fantasy shop that maintains an inventory of items that must be updated daily along with some a request to implement a new feature as well as some rules regarding what can and cannot be changed in the existing code. Most notably, the original Item class could not be changed. The instructions are clear to read so I will not elaborate any further.

 ## Understanding the Existing Codebase

 Once I knew the context for the task as hand the next step was to read and understand the existing code currently in use to solve the task. As one can see in the original repo the code consists of two classes, a GildedRose class for the shop and one Item class for items to be used in the inventory as well as separate file containing a unit test class with an example unit test. In evaluating the existing code I went through and added comments line-by-line to explain what was happening at each step. These notes can be found in the `gilded_rose_orgiginal.py` file.

 Most of the code was simple and self-explanatory with the main refactorable component being the `update_quality` method. This method consisted of a large series of nested if-statements. My first observation was that this massive series of nested if-statements was incredibly hard to read and follow. Next, I could see that most, if not all, values were hard-coded into the method. This is a big problem as if one value is updated but the others are not the code can easily break, even from a small typo. I will address more about the code and my work to improve it in the Refactoring section.

## Unit Testing

 Once I understood what the code did it was time to write the initial unit tests. This was to ensure the current code worked and behaved as expected, which the code did in fact work as described! Further, it was important to write initial unit tests using the original code so that my refactored code would behave the same way, validated using the same tests. These initial unit tests were not altered once I began refactoring. Because the instructions left out some details I opted to make my code behave exactly as the original did.

 Through out the process, anytime I added additional methods I also included unit tests to accompany them and tested at every step of the way to ensure my changes did not break the original functionality or to simply test my extra helper functions. As I had various iterations with different methods some unit tests were added and removed during the process. The ones remaining in the `test_guilded_rose.py` file are the final ones I used.

 ## Refactoring

 To begin with my refactoring I first did a few "house cleaning" steps to try to improve the readability and resilience of the code. This included:

 - Replacing repeated hard-coded strings with variables, leaving the strings to be written only once
 - Replacing some hard-coded numbers with variables, such as min and max values for quality and day intervals for the sale of backstage passes
 - Replacing self-updating variables with incremental and decremental operators like so: `item.quality = item.quality + 1` becomes `item.quality += 1`
 - Changing the backstage pass interval variables from `<11` and `<6` to `<=10` and `<=5` respectively. This helped to make the interval parameters more intuitive as day 10 and day 5.

While removing hard-coded values, I moved them to the top to be accessible as class variables (specifiable parameters of the shop). This would make it easier for any future updates to be made in one place in which the changes would permeate throughout the code.

 After this was complete the code was slightly better but there was a much bigger issue to deal with. The large sequence of nested if-statements was incredibly difficult to read and thus made for very unmaintainable code. My next task was to redesign how the updates were to be handled.

 ### Attempt 1

 To begin tackling the main refactor it was important to examine the overall structure and behavior of the program. Essentially we had a shop with items that were updated daily in which different item categories had different daily update behavior. Considering that the objects were represented as Item objects I thought the most natural approach would be to utilize object oriented programming. This way, each item could take on its own unique characteristics depending on which category of item it was.

 One of the first issues I encountered with this approach was that the rules specifically state that I was not able to edit the Item object. So, I thought to polymorphism and extend the Item object to a series of specific item types, these being Normal Items, Conjured Items, and Special Items. I wrote some new child-classes and began to experiment with them. I wanted to ensure that items used to initialize the GildedRose object could always be simple Item types in which I would later convert them to their specific category object but I found that Python does not exactly support casting in the way that I wanted to use it, meaning I could not easily take an Item object and convert it to a Normal object with ease.

 I think there is a way to accomplish this but I felt it would be far more time-consuming and perhaps over-engineered for the task at hand. An even simpler solution I wanted to implement was to add an instance variable to the Item class to designate the item's category but this was against the rules. While this was a good idea and could possibly be a good strategy if building from scratch, I felt that there would be a better and simpler way than to extend the Item class.

 ### Attempt 2

 Moving away from polymorphism I returned to the main GildedRose class to see what I could do to handle the item updates from within this class. Knowing that each item would be of a specific category I decided that I needed a way to determine an incoming item's category and handle the updates in accordance with the item category.

 The first method I added decided an item's category by means of its name, as this was the only identifying attribute. This way I could modularize each item type's update logic and process items based on the identified type. Because the instructions did not indicate what items names would typically be outside of a few examples, I made my own conclusions based on naming conventions as such:

  - Items with `sulfuras` in the name would be handled as a Sulfuras type item
  - Items with `backstage` in the name would be handled as a Backstage Pass type item
  - Items with `aged brie` in the name would be handled as an Aged Brie type item
  - Items with `conjured` in the name would be handled as a Conjured type item
  - Anything else would be handled as a normal type item

This iteration was something similar to this:
```python
def update_by_category(item):
      # crude string parse to get item category
      # handles one of 5 cases
      name = item.name.lower()
      if "sulfuras" in name:
          # handle sulfuras item
      elif "backstage" in name:
          # handle backstage pass item
      elif "aged brie" in name:
          # handle aged brie item
      elif "conjured" in name:
          # handle conjured item
      else:
          # handle normal item
```

From here I could move on to modularize each type's logic into their own methods. I began writing additional methods that would take in an Item object and perform the instance variable updates with the same restrictions in place as the nested if-statements. This way I could loop though the items, identify the type and and update accordingly, much like the original logic but in a cleaner, modularized way. In this iteration I wrote 5 methods: normal item updates, conjured item updates, brie item updates, backstage pass updates, and a sulfuras item update.

These methods made it much easier to locate each item type's specific logic but there was still a big problem; lots of repetitive code! With these 5 methods before me I could see much room for improvement by further modularizing the repetitive behavior in across each method.

I observed that items either went up or went down in quality, thus I wrote specific functions to increase or decrease quality. Within the increasing or decreasing methods I also implemented safeguards to prevent values from going outside the shop's set boundaries for quality (a 0 to 50 range). These looked something like this:

```python
def decrement_quality(item, val):
      # decrease quality by val; prevents going below 0
      stageUpdateVal = item.quality - val
      if stageUpdateVal < minQuality:
          item.quality = minQuality
      else:
          item.quality -= val

  def increment_quality(item, val):
      # increase quality by val; prevents going over 50
      stageUpdateVal = item.quality + val
      if stageUpdateVal > maxQuality:
          item.quality = maxQuality
      else:
          item.quality += val
}
```

These functions updated the the quality by whatever value was specified while also keeping within each boundary. I did think that these could possibly be combined into a single method but I felt that keeping them separate aided readability when called elsewhere.

Next, I could see repetitive behavior in items such as Aged Brie, Conjured Items, and Normal Items. Each of these three items simply increased or decreased in quality based on their respective rates of change and what day it was; prime candidates for consolidation. Thus, I wrote a method `update_basic` which could handle these three items types and adapt by simply using some method parameters. This took the form of:

```python
def update_basic(item, direction, rate_pre, rate_post):
    # update quality based on increasing/decreasing and sell_in val
    if direction == 'inc':
        if item.sell_in <= 0:
            increment_quality(item, rate_post)
        else:
            increment_quality(item, rate_pre)
    elif direction == 'dec':
        if item.sell_in <= 0:
            decrement_quality(item, rate_post)
        else:
            decrement_quality(item, rate_pre)
    # update sell_in
    update_sell_in(item)
```
Here, the function could handle the 4 cases: increasing/decreasing and before/after sell by date using their respective rates. Of course after quality was updated the `sell_in` attribute is updated.

A quick note about updating `sell_in`: This value update was essentially the same for each item, counting down days. Thus to remove hard-coded values throughout I wrapped this update in a small helper function called `update_sell_in`; this way its behavior could be managed in one location.

Following this, it was time to tackle the backstage passes, the most complex logic of any item. For this item type I made a unique method to hand the updates as it had more complex update logic based on the number of days until the concert. In this method I still utilized my incremental updating method to change the quality values but it has its own logic to determine how much to update. To determine how much to increment (or convert to 0) I used a simple series of if...elif statements to place the item in its proper interval and update the quality accordingly. This began by using traditional interval logic in which the statements checks if the `sell_in` is less than or greater than the days in the specified interval. This worked fine but I thought it looked ugly and was hard to read quickly and this opted for Python's native bisect package, which gives a cleaner (and fast!) look. This ended up looking something like this:

```python
def update_backstage(item):
      # update quality based on sell_in's place in defined intervals
      intvl = [0, 5, 10]
      if bisect.bisect_left(intvl, item.sell_in) == 0:
          item.quality = 0
      elif bisect.bisect_left(intvl, item.sell_in) == 1:
          self.increment_quality(item, 3)
      elif bisect.bisect_left(intvl, item.sell_in) == 2:
          self.increment_quality(item, 2)
      elif bisect.bisect_left(intvl, item.sell_in) == 3:
          self.increment_quality(item, 1)
      # update sell_in
      update_sell_in(item)
```

Finally, the last item type, Sulfuras, was simple. This item was not subject to any changes and thus this specific handler method did nothing but pass over the object. The instructions state that the value does not change from 80 quality and does not need to be sold, which took to mean that neither value needed to be update. The function looked as follows:

```python
def update_sulfuras(item):
      # No action required for Sulfuras
      pass
```

Once item types could be identified and handled according to their specific logic it was time to put them together. I was able to maintain the original method call that updated all the items in the shop just as the original code did while also not touching the `items` instance variable (as required in the rules). To do this I simply looped though like before but rather than nested if-statements, the `update_by_category` method could identify each item type and update accordingly. All of my original unit tests passed with no errors. Excellent!

### Additional Thoughts

One thing I am aware of but did not handle was input value enforcement. What I mean by this is that I assume items being input into the system will abide by the rules, such as having quality between 0 and 50, Sulfuras at a quality of 80 etc.. While I could have spent the extra effort to build such protection, and normally would in a real application, I though it would be sufficient to focus on the refactoring and handing of the item updates while assuming that incoming objects would fall within their respective boundaries.
