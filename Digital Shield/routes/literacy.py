from flask import Blueprint, jsonify

literacy_bp = Blueprint('literacy', __name__)

@literacy_bp.route('/')
def literacy_home():
    return jsonify({"message": "Digital Literacy Guide - Coming Soon!"})

@literacy_bp.route('/platforms')
def get_platforms():
    return jsonify({"platforms": ["WhatsApp", "Facebook", "Instagram", "Twitter/X", "TikTok"]})