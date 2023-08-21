from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import os
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.form
    generatedResponse = generate_response(data.get('user_input'))
    return generatedResponse


def generate_response(prompt):
    model = GPT2LMHeadModel.from_pretrained('./model')
    tokenizer = GPT2Tokenizer.from_pretrained('./model')
    # Create the attention mask and pad token id
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones_like(input_ids)
    output = model.generate(
        # max_length=256,
        # num_beams=4,
        # attention_mask=attention_mask,
        # num_return_sequences=1,  # Generate a single sequence
        # temperature=0.9,       # Controls randomness (higher for more diversity)
        # early_stopping=True,
        input_ids,
        max_length=256,
        num_beams=4,
        attention_mask=attention_mask,
        num_return_sequences=1,  # Generate a single sequence
        temperature=1,       # Controls randomness (higher for more diversity)
        top_k=50,
        top_p=0.92
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    if len(response) > 0:
        return jsonify({'message': re.findall(r'(?<=\[<startoftext>])(.*?)(?=\[<endoftext>])', response)[0]})
    else:
        return jsonify({'message': 'I couldn\'t answer that!'})


if __name__ == '__main__':
    app.run(debug=True)
