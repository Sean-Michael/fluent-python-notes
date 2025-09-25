# Chapter 1: The Python Data Model

Special methods, called "dunders" can be used to leverage the Python Data Model. They provide:

- standardized operations like `__getitem__`
- benefit from standard library functions like `random.choice`

Infix operators like + `__add__` and * `__mul__` create new objects and do not touch ther operands. In example 1.2 [[vector2d.py]] the addition and multiplication return a new `Vector` object that is the result of the operation. They do not actually modify the original `self`. 

The `__repr__` special method uses *f-string* notation `!r` to get the standard representation of the value so that we have `Vector(1, 2)` rather than `Vector('1', '2')`. 

> The string returned by `__repr__` should be unambiguous and, if possible, match the source code necessary to re-create the represented object. 

> In contrast, `__str__` is called by str() built-in and implicitly used by the print function. It should return a string suitable for dislay to end users.


## Questions:

1. How does the `in` operator work without `__contains__`?

> Implicit iteration, if a collection has no `__contains__` method, the `in` operator does a sequential scan.

- So as long as it's iterable the `in` operator can work?
- What are the criteria for being 'iterable'? 

**Answer:**

Yes, as long as an object is iterable, the `in` operator can work! When Python doesn't find a `__contains__` method, it falls back to iteration. Here's what makes something iterable:

- Having `__iter__` method (returns an iterator), OR
- Having `__getitem__` method that accepts integer indices starting from 0

Your `FrenchDeck` class is iterable because it has `__getitem__`. When you do `card in deck`, Python essentially does this fallback:

```python
# Python tries: deck.__contains__(card) - not found
# So it falls back to: iterate through deck and check each item
```

2. How does the `spades_high` sorting function work?

How the fuck does this work? 

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
for card in sorted(deck, key=spades_high):
    print(card)
```

- I'm a little bit confused on how sorted is used, the key is a function? So we're calculating a numbered ranking with this function?
- So how exactly is this function working? I sort of understand the rank-value based on the index of the ranks list. but the return is confusing me.

**Answer:**

Yes, the `key` parameter in `sorted()` takes a function! This function calculates a numeric "sort value" for each card. Let's break down `spades_high`:

```python
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)  # 0-12 (2 through A)
    return rank_value * len(suit_values) + suit_values[card.suit]
```

The math creates a unique number for each card:
- `rank_value * 4` gives: 0, 4, 8, 12... (spacing for suit rankings)
- `+ suit_values[card.suit]` adds: 0(clubs), 1(diamonds), 2(hearts), 3(spades)

So a 2 of clubs = `0 * 4 + 0 = 0`, while 2 of spades = `0 * 4 + 3 = 3`. This ensures spades always rank higher than other suits of the same rank.

The function transforms each card into a number that `sorted()` can use to order them correctly!

The multiplication by 4 (number of suits) ensures that **rank always takes precedence over suit**.

Here's why this matters:

**Without the `* 4` multiplication:**
- Ace of clubs = `12 + 0 = 12`
- King of spades = `11 + 3 = 14`
- King of spades would be higher than Ace of clubs! ❌

**With the `* 4` multiplication:**
- Ace of clubs = `12 * 4 + 0 = 48`
- King of spades = `11 * 4 + 3 = 47`
- Ace of clubs is correctly higher than King of spades ✅

The multiplication creates "gaps" between rank values:
- All 2s: 0, 1, 2, 3
- All 3s: 4, 5, 6, 7
- All 4s: 8, 9, 10, 11
- ...
- All Aces: 48, 49, 50, 51

This way, the lowest card of a higher rank (like 3 of clubs = 4) is always greater than the highest card of a lower rank (like 2 of spades = 3).

The pattern is: **primary sort key × gap size + secondary sort key**. It's a common technique for creating compound sort orders where one criterion completely dominates another.

3. How do you come up with that kind of algorithm?

**Answer:**

This algorithm pattern is actually quite standard and has a name: **lexicographic ordering** (like dictionary ordering). Once you recognize the pattern, it becomes much easier to apply.

The general formula is:
```
primary_value * size_of_secondary_range + secondary_value
```

**Common examples where this pattern appears:**

1. **Time:** `hours * 60 + minutes` (to compare times)
2. **Coordinates:** `row * num_columns + column` (2D array to 1D index)
3. **Version numbers:** `major * 1000 + minor * 100 + patch`
4. **Alphabetical sorting:** `'AB' = A_value * 26 + B_value`

**How to think about it:**
1. Identify your primary sort criterion (rank)
2. Identify your secondary sort criterion (suit)
3. Ask: "What's the range of my secondary values?" (4 suits = 0,1,2,3)
4. Multiply primary by that range size to create gaps
5. Add secondary to fill those gaps

**Why it works:** The multiplication ensures the "jump" between primary categories is always bigger than any possible secondary difference.

This is a fundamental computer science pattern for creating **total ordering** from multiple criteria. You'll see it everywhere once you recognize it! The key insight is that you need gaps large enough that no secondary value can "leap over" to the next primary category.