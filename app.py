from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 配置（可从环境变量读取）
APP_PORT = int(os.environ.get('PORT', 5000))
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

# 模拟的捐赠记录存储（在实际中应使用数据库）
donations = []

@app.route('/')
def index():
    """根路径重定向到捐赠页面"""
    return render_template('donate.html')

@app.route('/donate')
def donate_page():
    """捐赠页面"""
    return render_template('donate.html')

@app.route('/api/donate', methods=['POST'])
def process_donation():
    """处理捐赠API"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        # 简单验证
        if not amount or amount <= 0:
            return jsonify({'success': False, 'message': '金额无效'}), 400
        
        # 记录捐赠（实际中这里应集成支付网关或数据库）
        donation_record = {
            'amount': amount,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'pending'  # 在实际场景中，等待支付确认
        }
        donations.append(donation_record)
        
        # 模拟支付重定向或二维码生成逻辑
        # 在这里，我们返回一个成功响应，前端会展示微信二维码
        return jsonify({
            'success': True,
            'message': '捐赠请求已接收，请使用微信扫码支付',
            'amount': amount,
            'qr_data': f'weixin://donation/amount/{amount}'  # 模拟微信支付链接
        })
    
    except Exception as e:
        app.logger.error(f"捐赠处理出错: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT, debug=DEBUG_MODE)