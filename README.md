# Ingredientizer-USDA
This project was developed in collaboration with the Lemay lab, part of the USDA immunity and disease prevention unit, for obtaining ingredient lists of dishes. All scripts are written in Python and were run using Python version 3.10. This method and handle maps between lists of strings and lists containing lists of strings.</br>

Lists are obtained via the ChatGPT API so scripts will only run if the account associated with your API key has sufficient API tokens.</br>

## File descriptions
<ins>**get_ingredients_rate_limit.py**</ins> - this file contains a function called get_ingredients. When called, the function takes the first 3 dishes provided and makes sequential queries to obtain their ingredient lists. Once 61 second have passed, the process repeats for the next 3 dishes provided and so on. Before use, you will need to update your API key on line 4 and input the desired dish names into the list called original_test_foods on line 92. This file performs 3 queries per minute to work with the rate limit of 3 queries/min of some account types. The results of each query will be cleaned, have stop words removed (customize stop words by modifying the list called custom_stop_words on line 119), and the ingredients will be composed into a list. Once all queries are made, the resulting ingredient lists are saved with their corresponding dish name as a csv, which you will be prompted to name in your terminal, to your working directory.</br>

<ins>**get_ingredients_no_rate_limit.py**</ins> - this file is not limited to 3 queries per minute (it makes queries sequentially). This file contains a function called get_ingredients. When called, the function sequentially queries to obtain ingredient lists for each of the listed dishes. Before use, you will need to update your API key on line 4 and input the desired dish names into the list called test_foods on line 95. The results of each query will be cleaned, have stop words removed (customize stop words by modifying the list called custom_stop_words on line 112), and the ingredients will be composed into a list. Once all queries are made, the resulting ingredient lists are saved with their corresponding dish name as a csv, which you will be prompted to name in your terminal, to your working directory.

<ins>**get_synonyms.py**</ins> - this file creates a cvs containing lists synonyms for the terms provided in test foods list (on line 53) by querying ChatGPT for 10 synonyms for each term. The number of synonmys returned can be customized by modifying the prompt on line 8. This file does not accomodate rate limit restrictions. The purpose of this file is to create a food term thesaurus to enable more direct maps between databases in the future.
