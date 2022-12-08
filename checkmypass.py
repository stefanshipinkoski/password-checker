import requests
import hashlib
import sys
import pandas as pd


def requests_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error fetching {res.status_code}, check the API and try again ')
	return res


def get_pw_leaks_count(hashes, has_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == has_to_check:
			return count
	return 0

def pwned_api_check(password):
	#check password if it exists in API response
	sha1_pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_car, tail = sha1_pw[:5], sha1_pw[5:]
	response = requests_api_data(first5_car)
	return get_pw_leaks_count(response, tail)


def main(file):
	try:
		df = pd.read_csv(file)
		my_pw = df['password']
		my_pw.drop_duplicates(inplace=True)
		for password in my_pw:
			count = pwned_api_check(password)
			if count:
				print(f'{password} was found {count} times you should change your password')
	except AttributeError as err:
		err
if __name__ == '__main__':
	# read pw from text file or excel 
	main(sys.argv[1])
