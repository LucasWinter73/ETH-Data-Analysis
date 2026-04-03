# Data Analysis Cheetsheet - Lucas Winter

# Numpy intro

```python
import numpy as np
import matplotlib.pyplot as plt

# Arrays:
a = np.array([1, 2, 3, 4]) # 1D array
b = np.array([[1, 2, 3, 4], [5, 6, 7, 8]]) # 2D array

a = np.zeros(4) # generate 1D array with 4 zeros
b = np.ones((4, 2)) # generate 2D arrat with ones

c = np.linspace(0, 10, 5) # adds 5 values between 0 and 10 with equal distance

print(a[0]) # print 0th (1st) element of array a
print(a[0:2]) # prints all entries in a from 0th to 2nd

# loops
for ci in c:
  print(ci) # prints every entry in ci

for i, ci in enumerate(c):
  print(c[i]) #exactly the same as above
  
# functions
def function_name(parameter1, parameter2, keywordargument=initialvalue):
  # some code
  return return_value_1, return_value_2

# load and store data:
x1 = np.linspace(0, 2, 101) # store some data in x1
y1 = x1**2

np.savetxt('DataOut.txt', (x1, y1), delimiter = ',') # store file without header
np.savetxt('DataOutHeader.txt', (x1, y1), delimiter = ',', header='Exampledata')

(x2, y2) = np.loadtxt('DataOut.txt', delimiter = ',') #store our x1 and y1 in x2 and y2
(x3, y3) = np.loadtxt('DataOutHeader.txt', delimiter = ',', skiprows = 1) # skip row...

# load flie outside of cwd
import os # make any files accessible when searching...
(x4, y4) = np.loadtxt(os.path.join(path, 'DataOut.txt'))


# generate Histograms:
gz = np.loadtxt("data.txt") # Example data
N = len(gz) # get lenght of array
var = np.var(gz) * (N / (N - 1))

n_bins = 15 # amount of bins
bin_size = 0.005 # eidth of bins
bins = np.linspace(9.76, 9.76+bin_size*(n_bins - 1), n_bins)
	# create array of n_bins elemnts, distributed among the range of our measurment values
occurrence = np.zeros(n_bins) # create an array of 0s, the lenght of our bins
offset = np.min(bins)//bin_size + 1
	# take the smallest value in bins and devide it by width to a natural number and + 1.

for gx_i in gz:
  index = int(gx_i // bin_size - offset)
  occurrence[index] = occurence[index] + 1 # increase occurece by 1
  
A = N
g_theo = 9.78
plt.bar(bins, occurence / A, width = bin_size)
	# bins 								| 	x-position of each bar
  # occurence / A 			| 	height of each bar
  # width = bin_size 		| 	width of each bar

plt.vlines(g_theo, 0, np.max(occurence) / A)
plt.vlines(mean, 0, np.max(occurence) / A)
plt.vlines(mean + np.sqrt(var), 0, np.max(occurence) / A)
plt.vlines(mean - np.sqrt(var), 0, np.max(occurence) / A)
	# plt.vlines(x, ymin, ymax)
  # x 									| 	x-position where the line is drawn
  # ymin								| 	start of line on the y-axis
  # ymin								| 	end of line on y-axis

# Covariance:
# get some signals U1, U2, U3

C = np.stack((U1, U3), axis = 0)
cov13 = np.cov(C)
corcov13 = np.corrcoef(C)

D = np.stack((U1, U2), axis = 0)
cov12 = np.cov(D)
corcov12 = np.corrcoef(D)


# Auto-Kovarianz
def Rxx(x, delta):
  xm = np.mean(x)
  dev_sum = 0
  for i in range(len(x) - delta):
    dev_sum += (x[i] - xm) * (x[i + delta] - xm)
  return dev_sum / (len(x) - delta)

# use function on U1:
delta_max = len(U1)
Rxx_vs_delta = [Rxx(U1, i) for i in range(delta_max)]
lags = np.linspace(0, delta_max, num=delta_max)

# do a psd on some frequency:
FFTx = np.fft.fft(x) / N # normalized FFT of x(t)
PSD = dt * N * np.abs(FFTx)**2


```

## Example, measure g

```python
import numpy as np
import matplotlib.pyplot as plt

plt.plot(t, g) # plot timestamps and value of g from numpy array
N = len(g) # get lenght of array
# do it manually
mean = np.sum(g)/N # calculate mean with common formula
var = np.sum((g - mean)**2) / (N - 1) # calculate var with common formula

# use numpy functions
mean = np.mean(g)
var = np.var(g) * (N / (N - 1))

# Standartabweichung und Varianz
n_sigma = 0
width = 1
# iterate through all bins and add their values, if they are in the interval
i = 0
for b in bins:
  if (b >= (mean - np.sqrt(var) * width)) and (b <= (mean + np.sqrt(var) * width)):
    n_sigma = n_sigma + occurance[i]
  i += 1
  
# use random module for simulating values that have normal distribution:
g_sim = np.random.normal(mean, np.sqrt(var), N)
```



## NumPy Functions

### Array Creation
| Function              | Description            | Example                             |
| --------------------- | ---------------------- | ----------------------------------- |
| `np.array()`          | Create array from list | `np.array([1, 2, 3])`               |
| `np.zeros()`          | Array of zeros         | `np.zeros(5)` or `np.zeros([2, 3])` |
| `np.ones()`           | Array of ones          | `np.ones(5, dtype=int)`             |
| `np.arange()`         | Range with step size   | `np.arange(0, 5, 0.5)`              |
| `np.linspace()`       | Evenly spaced values   | `np.linspace(0, 5, 11)`             |
| `np.random.rand()`    | Random uniform [0,1)   | `np.random.rand(100)`               |
| `np.random.randint()` | Random integers        | `np.random.randint(0, 2, 10)`       |

### Array Operations
| Function    | Description                  | Example        |
| ----------- | ---------------------------- | -------------- |
| `np.diff()` | Differences between elements | `np.diff(arr)` |
| `np.sort()` | Sort array                   | `np.sort(arr)` |
| `np.min()`  | Minimum value                | `np.min(arr)`  |
| `np.max()`  | Maximum value                | `np.max(arr)`  |
| `np.sum()`  | Sum of elements              | `np.sum(arr)`  |
| `np.prod()` | Product of elements          | `np.prod(arr)` |
| `np.mean()` | Mean (average)               | `np.mean(arr)` |
| `np.std()`  | Standard deviation           | `np.std(arr)`  |
| `np.var()`  | Variance                     | `np.var(arr)`  |
| `np.sqrt()` | Square root                  | `np.sqrt(arr)` |
| `np.exp()`  | Exponential                  | `np.exp(arr)`  |
| `np.sin()`  | Sine                         | `np.sin(arr)`  |
| `np.abs()`  | Absolute value               | `np.abs(arr)`  |

### Array Manipulation
| Function          | Description        | Example                           |
| ----------------- | ------------------ | --------------------------------- |
| `np.append()`     | Append values      | `np.append(arr, new_val)`         |
| `np.fromstring()` | Create from string | `np.fromstring('1,2,3', sep=',')` |
| `np.shape`        | Get dimensions     | `arr.shape`                       |
| `len()`           | Get length         | `len(arr)`                        |

### Loading/Saving Data
| Function       | Description         | Example                                                      |
| -------------- | ------------------- | ------------------------------------------------------------ |
| `np.loadtxt()` | Load from text file | `np.loadtxt('file.txt', delimiter=',', skiprows=1)`          |
| `np.savetxt()` | Save to text file   | `np.savetxt('out.txt', data, delimiter=',', header='header')` |

## Array Indexing & Slicing

### 1D Array Indexing
| Syntax     | Description                  | Example                        |
| ---------- | ---------------------------- | ------------------------------ |
| `a[i]`     | Element at index i (0-based) | `a[0]` (first element)         |
| `a[-1]`    | Last element                 | `a[-1]`                        |
| `a[i:j]`   | Elements i to j-1            | `a[2:5]`                       |
| `a[i:]`    | From i to end                | `a[3:]`                        |
| `a[:j]`    | From start to j-1            | `a[:4]`                        |
| `a[i:j:k]` | Step k from i to j-1         | `a[1:8:2]` (every 2nd element) |

### 2D Array Indexing
| Syntax        | Description                | Example       |
| ------------- | -------------------------- | ------------- |
| `a[i, j]`     | Element at row i, column j | `a[0, 1]`     |
| `a[i, :]`     | Entire row i               | `a[0, :]`     |
| `a[:, j]`     | Entire column j            | `a[:, 0]`     |
| `a[i:j, k:l]` | Submatrix                  | `a[0:2, 1:3]` |
| `a[:, ::2]`   | Every 2nd column           | `a[:, ::2]`   |

## Matplotlib Functions

### Basic Plotting
| Function            | Description   | Example                         |
| ------------------- | ------------- | ------------------------------- |
| `plt.figure()`      | Create figure | `fig = plt.figure()`            |
| `fig.add_subplot()` | Add subplot   | `ax = fig.add_subplot(1, 1, 1)` |
| `ax.plot()`         | Line plot     | `ax.plot(x, y, 'x-')`           |
| `ax.scatter()`      | Scatter plot  | `ax.scatter(x, y, c=values)`    |
| `ax.bar()`          | Bar chart     | `ax.bar(x, height, width=0.8)`  |
| `ax.axvline()`      | Vertical line | `ax.axvline(x, color='r')`      |

### Plot Customization
| Function             | Description   | Example                              |
| -------------------- | ------------- | ------------------------------------ |
| `ax.set_xlabel()`    | X-axis label  | `ax.set_xlabel('Time (s)')`          |
| `ax.set_ylabel()`    | Y-axis label  | `ax.set_ylabel('Voltage (mV)')`      |
| `ax.set_title()`     | Plot title    | `ax.set_title('Data Plot', size=10)` |
| `ax.set_xlim()`      | X-axis limits | `ax.set_xlim(0, 10)`                 |
| `ax.set_ylim()`      | Y-axis limits | `ax.set_ylim(0, 100)`                |
| `ax.legend()`        | Add legend    | `ax.legend()`                        |
| `fig.tight_layout()` | Adjust layout | `fig.tight_layout()`                 |

### Formatting & Display
| Function               | Description       | Example                |
| ---------------------- | ----------------- | ---------------------- |
| `%matplotlib inline`   | Static plots      | `%matplotlib inline`   |
| `%matplotlib notebook` | Interactive plots | `%matplotlib notebook` |
| `plt.show()`           | Display plot      | `plt.show()`           |

## Python Built-in Functions Used

### Control Flow
| Function           | Syntax                     | Description              |
| ------------------ | -------------------------- | ------------------------ |
| `for` loop         | `for item in iterable:`    | Iterate over sequence    |
| `if`/`elif`/`else` | `if condition:`            | Conditional execution    |
| `range()`          | `range(start, stop, step)` | Generate number sequence |
| `enumerate()`      | `enumerate(iterable)`      | Get index and value      |

### File Operations
| Function       | Description    | Example                            |
| -------------- | -------------- | ---------------------------------- |
| `open()`       | Open file      | `with open('file.txt', 'r') as f:` |
| `readlines()`  | Read all lines | `lines = f.readlines()`            |
| `writelines()` | Write lines    | `f.writelines('text\\n')`          |

### OS Operations
| Function         | Description             | Example                                |
| ---------------- | ----------------------- | -------------------------------------- |
| `os.getcwd()`    | Get current directory   | `cwd = os.getcwd()`                    |
| `os.listdir()`   | List directory contents | `files = os.listdir(cwd)`              |
| `os.path.join()` | Join path components    | `path = os.path.join(cwd, 'file.txt')` |

### String Formatting
| Syntax      | Description       | Example                  |
| ----------- | ----------------- | ------------------------ |
| `.format()` | String formatting | `'{:.2f}'.format(value)` |
| `f-string`  | Formatted string  | `f'{value:.2f}'`         |

## Common Data Analysis Patterns

### Histogram Creation
```python
bin_edges = np.arange(min_val, max_val, bin_size)
hist, _ = np.histogram(data, bin_edges)
bin_centers = bin_edges[:-1] + 0.5 * bin_size
ax.bar(bin_centers, hist, width=bin_size * 0.8)
```

### Statistical Calculations

```python
mean = np.mean(data)
std = np.std(data)
# or custom:
N = len(data)
mean = sum(data) / N
variance = sum((x - mean)**2 for x in data) / N
std = np.sqrt(variance)
```

### Data Loading with Header

```python
data = np.loadtxt('filename.txt', delimiter=',', skiprows=1)
x = data[:, 0]  # first column
y = data[:, 1]  # second column
```

