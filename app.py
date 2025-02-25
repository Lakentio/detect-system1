from flask import Flask, request, jsonify
import platform
import os
import psutil  # Biblioteca para obter informações do sistema
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def detectar_distribuicao_linux():
    try:
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('NAME='):
                    return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
        pass
    return 'Linux (Distribuição não identificada)'

@app.route('/detectar-sistema', methods=['GET'])
def detectar_sistema():
    sistema = platform.system()
    arquitetura = platform.machine()
    num_nucleos = psutil.cpu_count(logical=False)
    memoria_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convertendo para GB

    if sistema == 'Linux':
        sistema = detectar_distribuicao_linux()

    return jsonify({
        'sistema_operacional': sistema,
        'arquitetura': arquitetura,
        'num_nucleos': num_nucleos,
        'memoria_ram': f'{memoria_ram} GB'
    })

if __name__ == '__main__':
    app.run(debug=True)