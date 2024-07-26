# app.py
from flask import Flask, request, jsonify
# from agent import BookingAgent
from openai_agent import BookingAgent

app = Flask(__name__)
# agent = BookingAgent()
agent = BookingAgent(api_key='<your-openai-api-key>')


@app.route('/chat', methods=['POST'])
def chat():
	data = request.json
	user_input = data.get('message', {}).get('content')
	chat_id = data.get('message', {}).get('id')

	if user_input and chat_id:
		response_content = agent.respond(user_input)
		response = {
			'message': {
				'content': response_content,
				'id': chat_id
			}
		}
		return jsonify(response)
	return jsonify({'error': 'Invalid input provided'}), 400

@app.route('/check_availability', methods=['POST'])
def check_availability():
	date = request.json.get('date')
	start = request.json.get('start')
	end = request.json.get('end')
	if date and start and end:
		available = agent.is_available(date, start, end)
		return jsonify({'available': available})
	return jsonify({'error': 'Missing date, start, or end'}), 400

@app.route('/book', methods=['POST'])
def book():
	name = request.json.get('name')
	date = request.json.get('date')
	start = request.json.get('start')
	end = request.json.get('end')
	if name and date and start and end:
		if agent.is_available(date, start, end):
			agent.bookings.append({'Name': name, 'Date': date, 'Start': start, 'End': end})
			return jsonify({'message': 'Booking confirmed!'}), 201
		else:
			return jsonify({'message': 'Time slot not available!'}), 409
	return jsonify({'error': 'Missing name, date, start, or end'}), 400

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
