#### Required Software information

This project uses the following IDE and python distribution:

**Python**

- IDE is Spyder 3
	- *How to install Spyder*: See [here](https://docs.spyder-ide.org/installation.html). 
		- Open a command prompt window and browse to your local python installation directory. In my case its, `c:\users\myusername\miniconda3` and then type `pip3 install spyder`
		- To launch spyder IDE, open a command prompt window, type the command, `spyder3` and hit the enter key. Spyder IDE will launch
		
- Python 3 distribution is Miniconda 3

#### General Folder & Variable naming conventions

This repository follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard for Python file and folder naming conventions. Also see the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations).

- A Python **File name** must have a `.py` extension and must not contain dashes (-). This allows them to be imported and unittested. It is also called a `module` . It is simply a Python source file, which can expose classes, functions and global variables.
	- Modules: should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Example: `my_module.py`
	- Function: Function names should be lowercase, with words separated by underscores as necessary to improve readability. Example: `my_function`
	- **Function arguments**: Always use `self` for the first argument to instance methods.
		- Always use `cls` for the first argument to class methods.
		- If a function argument's name clashes with a reserved keyword, it is generally better to append a single trailing underscore rather than use an abbreviation or spelling corruption. Thus `class_` is better than clss. (Perhaps better is to avoid such clashes by using a synonym.)
	- **Variable name**: use a lowercase single letter, word, or words. Separate words with underscores to improve readability. Example: `my_variable`
- A Python **package** is simply a directory of Python module(s).
	- Python packages should also have short, all-lowercase names, although the use of underscores is discouraged. Example: `mypackage`
	- **Constant** - Use an uppercase single letter, word, or words. Separate words with underscores to improve readability. Example: `MY_CONSTANT`
	- **Class** - start each word with a capital letter. Do not separate words with underscores. This style is called camel case. Example: `MyClass`  

