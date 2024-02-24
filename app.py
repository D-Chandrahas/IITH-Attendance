from flask import Flask, request

app = Flask(__name__)

@app.route('/MobileAPI/GetMobileAppValidatePassword', methods=['POST'])
def hello():
    request_body = request.data.decode('utf-8')
    print(request.headers)
    print(request_body)
    return {"Webidentifier": "1234"}

if __name__ == '__main__':
    app.run(debug=True)