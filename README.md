Sublime Text 2 : Python Test Runner
===================================

Overview
--------
Running Python unit tests (all tests from file or single test). Also running last test.

Support Linux ans OS X. Windows will be in near future.

Author:
-------
* Taras Lyapun (http://lyapun.com/)

Installation
------------

Go to your Sublime Text 2 `Packages` directory

 - OS X: `~/Library/Application\ Support/Sublime\ Text\ 2/Packages`
 - Linux: `~/.config/sublime-text-2/Packages/`

and clone the repository using the command below:

``` shell
git clone https://github.com/lyapun/sublime-text-2-python-test-runner.git PythonTestRunner
```

Settings
--------

You can set plugin settings and project level, because, probably, you need different settings for different projects.

You should add section "python_test_runner" into "settings" section.
 And you can specify:

"test_command" - by default is "nosetests".

"test_root" - by default you project root.

"before_test" - before test hook (eg activate env)

"after_test" - after test hook (ag deactivate env)

"test_delimeter" - delimeter which separates test file and test class. E.g. for nosetests is ":", for django default test runner: ".".

Usage
-----

- Run single python test: `Command-Shift-R` (or `Ctrl-Shift-R` for Linux)
- Run all python tests from current file: `Command-Shift-T` (or `Ctrl-Shift-T` for Linux)
- Run last python test: `Command-Shift-E`

Also you can run tests from context menu, sublime menu (Tools), or command pallete.

Project settings example:
-------------------------

 my-project.sublime-project

	{
		"folders":
		[
			{
				"path": "TestProject"
			}
		],
    	"settings": 
    	{   
        	"python_test_runner": 
        	{
            	"before_test": "source .env/bin/activate",
            	"after_test": "deactivate",
            	"test_root": "/Path/To/Project",
            	"test_delimeter": ":",
            	"test_command": "make test test="
        	}
    	}
	}
	
ToDo list:
----------
- Add support for Windows