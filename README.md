# unixreg

## why
While working on porting a python application to Linux I came across many uses of winreg that could not easily be ported over.

Instead of reworking the system I decided to implement a bandaid solution that deals with it transparently.

## how to use
Update your winreg imports with this

```py
try:
	import winreg
except ImportError:
	import unixreg as winreg
```

simply importing unixreg should be enough though, winreg is imported if found

## license
this project is licensed under the [MIT License](LICENSE)  
feel free to do whatever you want with it
