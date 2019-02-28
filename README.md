# Adding Text to PDF

This script is for adding card number on a visitor card.
To make this file work you need to add "cards" folder in the main folder. 
First you create a Card object as in the example
```python
card = Card()
```

To create only one file you need to use
```python
card.build_pdf_to_merge()
```

To create batch of files you need to use. Parameter represents the number of cards.
```python
card.build_batch(500)
```

To merge al files in cards/ folder
```python
card.merge_all_files()
```
