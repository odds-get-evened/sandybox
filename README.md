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

an example:

```python
plot = plots_3d(normalize_str(phrases['long_sentences'][0], t_min=0, t_max=9))  
plot2 = plots_3d(normalize_str(phrases['long_sentences'][1], t_min=-1, t_max=1))  
print(plot)  
print(plot2)
```

produces:

```shell
[[8.096843924804473, 6.947965652638584, 0.42273776792798096], [5.138550513367767, 5.012731974240862, 0.42862722056567554], [4.653967865359287, 0.48231160612554413, 8.71938156857367], [8.714223022138325, 0.015702012070459105, 4.8385553544813975], [0.6599462700191603, 5.9970577429550085, 8.08248159573283], [6.239993329482605, 5.836915325661324, 7.814023666972756], [1.284120143791817, 3.3245180363086466, 0.0], [6.055784050504046, 7.3851053980474894, 0.18421874076955377], [9.0, 5.692570345973751, 7.038084172689894], [7.986155091376567, 4.040384652765208, 0]]

...

[[0.11405389252307119, 0.4587381913012396, 0.8868128445201044], [-0.05505694342822465, -0.6066624012663495, -0.6326213787235562], [0.7978999549766348, -0.794050860646101, 0.2264911620687271], [-0.5843822589647198, -0.8255583555137633, 0.17183784735419394], [0.4829137354855815, -1.0, -0.8552494787206317], [-0.66754430103652, -0.8536306049566738, -0.18424649710895968], [-0.8140191062313222, -0.969932376165421, -0.7029154667778896], [1.0, 0.9956103618426784, 0.6736560772787044]]
```

**hashies**

turn bytes into big endian 64 bit data types

```python
def big_end_int_64(data: bytes) -> int:

def big_end_bytes_64(data: bytes) -> bytes:

def big_end_str_64(d: bytes) -> str:

def big_end_hex_64(d: bytes) -> str:
```