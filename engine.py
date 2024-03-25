import asyncio
from sympy import sympify, symbols
import secrets
import time
import math
import random

def test():
	x, y = symbols('x y')

	formulas = [
		'xy',
		'2*(x-y)',
		'x**2+y**2',
	]
	
	expr = sympify(formulas[1])
	print(expr.evalf(subs={x: 2, y: 1}))
	
def sigmoid(n):
	return 1 / (1 + math.exp(-n))
	
def tanh(n):
	return (math.exp(n) - math.exp(-n)) / (math.exp(n) + math.exp(-n))
	
def relu(n):
	return max(0, n)
	
def leaky_relu(n, alpha=0.1):
	return max(x, alpha * n)
	
def softmax(n):
	e_x = [math.exp(v) for v in n]
	
	return [v / sum(e_x) for v in e_x]
	
class Heartbeat:
	def __init__(self):
		self.result = 0
		
		asyncio.run(self.start())
		
	async def start(self):
		random.seed(time.time())
		
		start_time = time.time()
		
		rand = random.uniform(-1, 1)
		threshold = random.uniform(-1, 1)
		
		print(f"random: {rand}; tanh: {tanh(rand)}; sigmoid: {sigmoid(rand)}; threshold: {threshold}")
				
		span = time.time() - start_time
		print(f"timespan: {span}")
	
def do_heartbeat():
	hb = Heartbeat()

def main():
	do_heartbeat()
	
if __name__ == "__main__":
	main()