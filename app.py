from flask import Flask, render_template, request, jsonify
from point import Point
from ecc_operations import find_base_point, find_n, generate_curve, generate_keys, sign, verify, generate_prime

app = Flask(__name__)

generated_private_key = None
generated_public_key = None
curve_params = None
G = None
n = None

@app.route('/')
def index():
    global curve_params, G, n
    p = int("0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)
    a = int("0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc", 16)
    b = int("0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00", 16)
    G = Point(int("0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66", 16), 
              int("0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650", 16), (a, b, p))
    n = int("0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409", 16)
    # p = generate_prime(13)
    # a, b = 1, 7
    # G = find_base_point(a, b, p)
    # n = find_n(G)

    curve_params = {'a': a, 'b': b, 'p': p}
    return render_template('index.html', curve_params=curve_params)

@app.route('/generate_keys', methods=['POST'])
def generate_keys_endpoint():
    global generated_private_key, generated_public_key, G, n
    d, Q = generate_keys(G, n)
    generated_private_key = d
    generated_public_key = {'x': Q.x, 'y': Q.y}
    str_generated_public_key = {'x': str(Q.x), 'y': str(Q.y)}
    return jsonify({
        'private_key': str(d),
        'public_key': str_generated_public_key,
        'base_point': {'x': str(G.x), 'y': str(G.y)},
        'n': str(n)
    })

@app.route('/sign_message', methods=['POST'])
def sign_message():
    global generated_private_key, G, n
    if not generated_private_key:
        return jsonify({'error': 'Keys not generated yet!'}), 400

    data = request.json
    message = data.get('message')
    r, s = sign(message, generated_private_key, G, n)
    return jsonify({"r": str(r), "s": str(s)})

@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    global generated_public_key, G, n
    data = request.json
    message = data.get('message')
    r = int(data.get('r'))
    s = int(data.get('s'))
    use_generated_key = data.get('use_generated_key', True)
    
    if use_generated_key:
        if not generated_public_key:
            return jsonify({'error': 'Generated public key not available!'}), 400
        Q = Point(generated_public_key['x'], generated_public_key['y'], (curve_params['a'], curve_params['b'], curve_params['p']))
    else:
        public_key = data.get('public_key')
        Q = Point(public_key['x'], public_key['y'], (curve_params['a'], curve_params['b'], curve_params['p']))

    result = verify(message, r, s, Q, G, n)
    print(f"Q: {result}")
    return jsonify({'valid': result })

if __name__ == '__main__':
    app.run(debug=True)
