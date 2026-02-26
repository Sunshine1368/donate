from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

APP_PORT = int(os.environ.get('PORT', 5000))
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

# 存储捐赠记录（内存列表，重启即丢失。生产环境请替换为数据库）
donations = []

@app.route('/')
def index():
    return render_template('donate.html')

@app.route('/donate')
def donate_page():
    return render_template('donate.html')

@app.route('/api/donate', methods=['POST'])
def process_donation():
    try:
        data = request.get_json()
        name = data.get('name', '无名好心人').strip()
        amount = data.get('amount')
        
        if not name:
            name = '无名好心人'
        if not amount or amount <= 0:
            return jsonify({'success': False, 'message': '金额无效'}), 400
        
        # 记录捐赠
        donation_record = {
            'name': name,
            'amount': amount,
            'timestamp': datetime.utcnow().isoformat() + 'Z',  # ISO格式带Z表示UTC
            'status': 'pending'
        }
        donations.append(donation_record)
        
        # 可选：限制内存记录数量（保留最近100条）
        if len(donations) > 100:
            donations.pop(0)
        
        return jsonify({
            'success': True,
            'message': '捐赠请求已接收',
            'amount': amount
        })
    
    except Exception as e:
        app.logger.error(f"捐赠处理出错: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500

@app.route('/api/donations', methods=['GET'])
def get_donations():
    """返回最近10条捐赠记录（按时间倒序）"""
    try:
        # 按时间戳倒序，取前10条
        sorted_donations = sorted(donations, key=lambda x: x['timestamp'], reverse=True)[:10]
        return jsonify({'donations': sorted_donations})
    except Exception as e:
        app.logger.error(f"获取捐赠列表出错: {e}")
        return jsonify({'donations': []}), 200  # 出错时返回空列表

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT, debug=DEBUG_MODE)