import re
import nltk
from nltk.corpus import stopwords
from oddles.hashies import big_end_int_64
# import numpy as np

def normalize_arr(arr, t_min, t_max):
	norm_arr = []
	
	diff = t_max - t_min
	diff_arr = max(arr) - min(arr)
	
	for i in arr:
		temp = (((i - min(arr)) * diff) / diff_arr) + t_min
		
		norm_arr.append(temp)
		
	return norm_arr

def normalize_str(s: str) -> list[int]:
	# all to lowercase
	s = s.lower()
	# remove numbers
	s = re.sub(r'\d+', '', s)
	# remove everything except words and spaces
	s = re.sub(r'[^\w\s]', '', s)
	
	stopw = set(stopwords.words('english'))
	# remove stopwords and convert all strings to integer hash
	s_ls = [big_end_int_64(w.encode('utf8')) for w in s.split(' ') if w not in stopw]
	# normalize
	s_ls = normalize_arr(s_ls, -1, 1)
	
	return s_ls
	
def plots_2d(arr):
	new_arr = []
	
	for i in range(len(arr)):
		plot = None
		
		if i*2 < len(arr):
			plot = [arr[i*2]]
			
		if i*2+1 < len(arr):
			plot.append(arr[i*2+1])
			
		if plot is not None:
			new_arr.append(plot)
	
	return new_arr
	
def plots_3d(arr):
	new_arr = []
	
	for i in range(len(arr)):
		plot = None
		
		if i*3 < len(arr):
			plot = [arr[i*3]]
			
		if i*3+1 < len(arr):
			plot.append(arr[i*3+1])
			
		if i*3+2 < len(arr):
			plot.append(arr[i*3+2])
		
		if plot is not None:
			new_arr.append(plot)
	
	return new_arr

def main():
	s = "You don’t have to be into the wilderness to enjoy camping. Tom doesn't want to make a big deal out of it. Our competitors don't normally ask us for advice, but when an airline leader reached out, we couldn't ignore it."
	print(plots_3d(normalize_str(s)))
	print(plots_3d([_ for _ in range(10)]))
	
	

if __name__ == "__main__":
	main()