# Multilingual Online Translator
Study project from [JetBrains Academy](https://hyperskill.org/projects/99)

## About
Everyone’s familiar with online translators. They giving us a handy way to translate on the go. In this project, you’re about to write an app that translates the words you type and gives you many usage examples based on the context.

## Examples
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

### Example 1

You can choose the number of translations and sentence pairs for a language. There should be just at least one translation and one sentence pair.
```
> python translator.py english french hello
French Translations:
bonjour
allô
ohé
coucou
salut

French Examples:
Well, hello, freedom fighters.:
Et bien, bonjour combattants de la liberté.

Goodbye England and hello the Netherlands...:
Au revoir l'Angleterre et bonjour les Pays-Bas...

Yes, hello. Jackson speaking.:
Oui, allô, Jackson à l'appareil.

Hello, hello, hello, hello.:
Allô, allô, allô, allô.

And began appearing hello kitty games online.:
Et a commencé à apparaître bonjour Kitty jeux en ligne.
```

### Example 2
```
> python translator.py english korean hello
Sorry, the program doesn't support korean
```

### Example 3
```
> python translator.py english all hello
Something wrong with your internet connection
```

### Example 4
```
> python translator.py english all brrrrrrrrrrr
Sorry, unable to find brrrrrrrrrrr
```