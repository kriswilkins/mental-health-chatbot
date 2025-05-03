from quart import render_template, request, jsonify, session # type: ignore
from app import app
from app.chatbot import get_chatbot_response
import os
import asyncio
import re

@app.route('/')
async def index():
    session.clear()
    session['greeted'] = False
    return await render_template('index.html')

@app.route('/chat', methods=['POST'])
async def chat():
    user_input = (await request.json).get('message')

    if not user_input:
        if not session.get('greeted', False):
            session['greeted'] = True
            return jsonify({'response': "Hello! What's your name?", 'sentiment': 'neutral'})
        return jsonify({'error': 'User input is empty'}), 400

    conversation_history = session.get('conversation_history', [])
    user_name = session.get('user_name')
    greeted = session.get('greeted', False)

    if not greeted:
        session['greeted'] = True
        return jsonify({'response': "Hello! What's your name?", 'sentiment': 'neutral'})

    if not user_name:
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"(\w+)"
        ]
        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                user_name = match.group(1).capitalize()
                session['user_name'] = user_name
                response = f"Nice to meet you, {user_name}! How can I help you today?"
                return jsonify({'response': response, 'sentiment': 'neutral'})
        
        response = "I'm sorry, I didn't catch your name. Could you please tell me your name?"
        return jsonify({'response': response, 'sentiment': 'neutral'})

    conversation_history.append(user_input)

    limited_history = conversation_history[-10:]

    response, sentiment = await get_chatbot_response(user_input)

    conversation_history.append(response)

    session['conversation_history'] = conversation_history

    return jsonify({'response': response, 'sentiment': sentiment})