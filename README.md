##### PythonF_ck

PythonF_ck is esoteric language based on Python 3+ using only 10 characters: __(ex'c+=%);__

Based on:  
* [Pyfuck](https://github.com/wanqizhu/pyfuck)  
* [Fewest (distinct) characters for Turing Completeness](https://codegolf.stackexchange.com/questions/110648/fewest-distinct-characters-for-turing-completeness/110722#110722)  
* [JSFuck](https://github.com/aemkei/jsfuck)
##### Example
Code below is simple `Hello world!`
```python3
c='%c';e=+(()==());ee=e;ex=ee+e;ec=ex+e;xe=ec+e;xx=xe+e;xc=xx+e;ce=xc+e;cx=ce+e;cc=cx+e;eee=cc+e;e=eee;eex=eee+e;eec=eex+e;exe=eec+e;exx=exe+e;exc=exx+e;ece=exc+e;ecx=ece+e;ecc=e
cx+e;xee=ecc+e;xex=xee+e;xec=xex+e;xxe=c%(cx+xee);xxx=c%(xe+xex);xxc=c%(xe+eec);xce=c%(ee+xex);xcx=c%(ex+xex);xcc=c%(xx+xee);cee=c%(xc+xex);cex=c%(ex+ece);cec=c%(ee+xee);cxe=c%(ex+ee
c);cxx=c%(cc+xex);cxc=c%(ec+eec);cce=c%(ee+exe);x=xcx+xxx+xcc+c%xex+cee+c%exe+xxc+cex+cec+xxe+xxe+xce+cxe+cxx+xce+xxx+xxe+c%xee+cxc+xxc+cce;exec(x)
```
##### Basics
```
False    =>  ()==''
True     =>  ()==()
0        =>  +(()=='')
1        =>  +(()==())
2        =>  +(()==())+(()==())
string   =>  ''
a        =>  '%c'%97 # where 97 is +(()==()) repeated 97 times
run      =>  exec()  
```
##### Explanation
1. Numbers  
   To provide numbers we can use tuple and empty string comparison and then cast it to integer value:
   ```python3
   >>> ()==''
   False
   >>> +(()=='')
   0
   >>> ()==()
   True
   >>> +(()==())
   1
   ```  
   All next numbers can be obtained with simple addition:
   ```python3
   >>> +(()==())+(()==())
   2
   >>> +(()==())+(()==())+(()==())+(()==())
   4
   ...
   ```
2. Characters  
   To cast numbers to string we use:
   ```python3
    >>> '%c' % 97
    'a'
    ```
3. Execution
    On this stage we can build full string with python code and execute it with `exec()`:
    ```python3
    >>> exec('%c'%110 + '%c'%61 + '%c'%55)
    >>> n
    7
    ```
4. Optimization  
    To reduce generated code size we can save used numbers in variables, which will be shorter than building every number from basics. 
    Most sources contain only ASCII characters from 1 - 129, so with only 213 initiation characters we can save further code length:
    ```
    ee = 1
    ex = 2
    ec = 3
    ...
    cc = 10
    eee = 20
    ...
    xee = 110
    xex = 120
    ``` 
    Rest of 3-character variables we can use to save most common chars in source code. For example:
    ```
    xec = 'e'
    xxe = 'i'
    ...
    ccc = '='
    ``` 
    Using 4-characters long would be unnecessary since we don't want to store all characters and it's possible to generate missing chars with saved numbers and casting them to string. 
5. Reserved variables
    e, x and c are reserved for
    * e - temporary for any math operations
    * x - accumulator for executed string
    * c - template for casting numbers to characters (`'%c'`)
