# sandybox

this collection of codes is meant to be a growing library of tools and small apps for reusability. if it can be applied more than once, it's getting thrown in here.

**lang**

normalizing language for machine learning and quantum plotting

```python
""" 
converts a 1-dimensional list to a 2-dimensional one, for plotting 3D coordinates """
def plot_2d(arr: list) -> list

""" 
convert a 1 dimensional list to a 2 dimensional one, for plotting 2D coordinates """
def plot_3d(arr: list) -> list

"""
using a natural language model (NLTK), converting text into a list of normalized number values
"""
def normalize_str(s: str, t_min=-1, t_max=1) -> list

""" 
bring an array of number values within a bounds constraint 
"""
def normalize_arr(arr: list, t_min=-1, t_max=1) -> list
```

**hashies**

turn bytes into big endian 64 bit data types

```python
def big_end_int_64(data: bytes) -> int:

def big_end_bytes_64(data: bytes) -> bytes:

def big_end_str_64(d: bytes) -> str:

def big_end_hex_64(d: bytes) -> str:
```