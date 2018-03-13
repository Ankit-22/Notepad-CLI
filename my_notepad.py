import requests

class my_notepad:

	_padLink = None

	def __init__(self, driver, padLink):
		if(my_notepad._padLink == padLink):
			return
		self.driver = driver
		self.padLink = padLink
		my_notepad._padLink = padLink
		self.driver.get("https://notepad.pw/"+self.padLink)
		page_source = self.driver.page_source;
		keyPosition = page_source.find('pad_key = ')
		self.padKey = page_source[keyPosition + 11 : keyPosition + 19]
		urlPosition = page_source.find('url_key = ')
		urlEnd = page_source[urlPosition + 11 : ].find("'")
		self.padLink = page_source[urlPosition + 11 : urlPosition + 11 + urlEnd]
		self.padContent = self.driver.execute_script("return $('.textarea').val()")
		caretPosition = page_source.find('caret = ')
		caretEnd = page_source[caretPosition + 8 : ].find(";")
		self.caret = page_source[caretPosition + 8 : caretPosition + 8 + caretEnd]

	def get_headers(self):
		headers = {
			"origin": "https://notepad.pw",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
			"user-agent": "Mozilla/5.0 (X11; Linux x86self._64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
			"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
			"accept": "*/*",
			"referer": "https://notepad.pw/"+self.padLink,
			"authority": "notepad.pw",
			"x-requested-with": "XMLHttpRequest"
		}
		cookie_list = self.driver.get_cookies()
		curlRequest = ""
		for cookie_json in cookie_list:
			curlRequest += cookie_json['name']+"="+cookie_json['value']+"; "
		curlRequest = curlRequest[:-2]
		headers['cookie'] = curlRequest
		return headers

	def get_updated_data(self):
		my_notepad._padLink = None
		self.__init__(self.driver, self.padLink)
		return self.padContent

	def send_data(self, contents):
		if self.padLink is None:
			print("No url detected")
			return
		headers = self.get_headers()
		data = {'pad': contents, 'key': self.padKey, 'pw': '', 'monospace': '0', 'url': self.padLink, 'caret': self.caret}
		req = requests.post('https://notepad.pw/save', data=data, headers=headers)
		print(self.get_updated_data())