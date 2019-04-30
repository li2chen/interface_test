import requests
import json
import os


def t_case(case_file=r'files\goods.json'):
	case_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), case_file)
	with open(case_file, 'r') as f:
		case = json.loads(f.read())
		# name = case['name']
		response = case['response']
		r_status = response['status_code']
		r_msg = response['body']['msg']

		req_data = {
			"url": case['request']['url'],
			"method": case['request']['method'],
			"headers": case['request']['headers'],
			"params": case['request']['data']}
		t_response = requests.request(**req_data)

		if r_status != '':
			assert r_status == str(t_response.status_code)
			for kv in r_msg.items():
				if kv[1] != '' and kv[0] == 'in':
					assert r_msg['in'] in t_response.text
				elif kv[1] != '' and kv[0] == 'not':
					assert r_msg['not'] not in t_response.text
				elif kv[1] != '' and kv[0] == 'eq':
					assert r_msg['eq'] == t_response.text


# current_json = t_response.json()
# json_diff = {}
# for key, expected_value in response['body'].items():
# 	print(response['body'].items())
# 	value = current_json.get(key, None)
# 	if str(value) != str(expected_value):
# 		json_diff[key] = {
# 			'value': value,
# 			'expected': expected_value
# 		}
# print(json_diff)


if __name__ == "__main__":
	t_case()
