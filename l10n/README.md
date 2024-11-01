# Localization (l10n) Tech Notes

## "Wrapping" text for translation
All you have to do in your code is wrap each piece of English text with the `gettext` shorthand `_()`:
* Wrap python strings: `error="No device was selected."` becomes `error=_("No device was selected.")`
* Use `.format()` to wrap strings with variable injections:
    ```python
    mystr = f"My dad's name is {dad.name} and my name is {self.name}."
    mystr = _("My dad's name is {} and my name is {}").format(dad.name, self.name)
    ```

    If there are a lot of variables to inject, placeholder names can be used:
    ```python
    mystr = _("My dad's name is {dad_name} and my name is {my_name}").format(dad_name=dad.name, my_name=self.name)
    ```
* Use `ngettext` to dynamically handle singular vs plural forms based on an integer quantity:
    ```python
    n = 1
    print(ngettext("apple", "apples", n))
    >> apple
    
    n = 5
    print(ngettext("apple", "apples", n))
    >> apples
    ```

Transifex will ask translators to provide the singular and plural forms.

Note: Some languages like Arabic have multiple plural forms (e.g. 2-3 is one form, > 3 is another).


## Understanding `gettext` wrapping
Note that this wrapping serves TWO purposes:
1. Pre-translation: This is how we identify text that translators need to translate. Any strings wrapped with `_()` (or related calls like `ngettext`) will appear in translators' Transifex UI.
2. Post-translation: It returns the locale-specific translation for that source string (defaults to the English string itself if no translation is available).

In general, most SeedSigner code uses the `_()` wrapping only to identify the strings that need translation.

The second step -- fetching the translated string -- mostly happens in the base `Screen` classes. They ask for the translation just before the text is drawn on screen.

Basic rules:
* Wrap raw English strings so they'll be picked up for translation.
* In general, don't go out of your way to pass already translated text to `Screen` classes.
  * The `Screen` itself should do most of the `_()` wrapping to translate its input attributes for final display.
* Basic gui `Component` classes (e.g. `Button`, `TextArea`) should ideally NOT wrap any text.
  * Ensure that they are supplied with wrapped / already translated text.

Basic example:
```python
@dataclass
class SomeClass:
   title: str = _("My Title")
```

In this case `title` is wrapped in order to get "My Title" into the translators' list. Note that because `title` is a class-level attribute, its string value will be determined at import time and
will NOT be re-evaluated when the class is eventually used. That means that the locale-specific translation will NOT be returned later:

```python
from blah import SomeClass

print(SomeClass.title)
>> My Title

# set locale to some other language and then...
os.environ['LANGUAGE'] = 'es'
my_instance = SomeClass()
print(my_instance.title)
>> My Title
```

To get the translated value, we'd have to pass the attribute itself into `_()`. This feels redundant since the original string was already wrapped in the class definition, but we have to
work around the realities of python imports, etc. This time the wrapping is saying, "Hey, take the value you're holding in that attribute/variable and see if it has an entry in our locale-specific
translation library."
```python
os.environ['LANGUAGE'] = 'es'
print(_(SomeClass.title))
>> Mi Titulo

my_instance = SomeClass()
print(_(my_instance.title))
>> Mi Titulo
```


## Set up localization dependencies
```bash
pip install -r l10n/requirements-l10n.txt
```

Make sure that your local repo has fetched the `seedsigner-translations` submodule. It's configured to add it in src/seedsigner/resources.
```bash
# Need --remote in order to respect the target branch listed in .gitmodules
git submodule update --remote
```


### Pre-configured `babel` commands
The `setup.cfg` file in the project root specifies params for the various `babel` commands discussed below.


### Rescanning for text that needs translations
Re-generate the `messages.pot` file:

```bash
python setup.py extract_messaages
```

This will rescan all wrapped text, picking up new strings as well as updating existings strings that have been edited.

_TODO: Github Action to auto-generate messages.pot and fail a PR update if the PR has an out of date messages.pot._


### Making new text available to translators
Upload the master `messages.pot` to Transifex. It will automatically update each language with the new or changed source strings.

_TODO: Look into Transifex options to automatically pull updates._


### Once new translations are complete
The translation file for each language will need to be downloaded via Transifex's "Download for use" option (sends you a `messages.po` file for that language).

This updated `messages.po` will need to be added to the seedsigner-translations repo in l10n/`{TARGET_LOCALE}`/LC_MESSAGES.


### Compile all the translations
The `messages.po` files must be compiled into `*.mo` files:

```bash
python setup.py compile_catalog

# Or target a specific language code:
python setup.py compile_catalog -l es
```

### Unused babel commands
Transifex eliminates the need for the `init_catalog` and `update_catalog` commands.


## Keep the seedsigner-translations repo up to date
The *.po files for each language and their compiled *.mo files should all be kept up to date in the seedsigner-translations repo.

_TODO: Github Actions automation to regenerate / verify that the *.mo files have been updated after *.po changes._

