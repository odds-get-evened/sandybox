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

def main():
	s = "You don’t have to be into the wilderness to enjoy camping. Tom doesn't want to make a big deal out of it. Our competitors don't normally ask us for advice, but when an airline leader reached out, we couldn't ignore it."
	print(normalize_str(s))
	
	

if __name__ == "__main__":
	main()