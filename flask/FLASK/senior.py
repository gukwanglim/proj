from flask import Flask, g, request, Response, make_response 
   
app = Flask(__name__)

app.config['SERVER_NAME'] = 'local.com:5002'

app.route("/sd")
def helloworld_local():
    return "Hello Local.com!"

@app.route("/sd", subdomain="g")
def helloworld22():
    return "Hello G.Local.com!!!"

@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)

@app.route('/test_wsgi')
def wsgi_test(): 
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]
    return make_response(application)
    
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

# @app.before_request
# def before_request():
#     print("before request!!!")
#     g.str = "한글"

@app.route("/gg")
def helloworld2():
    return "Hello World" + getattr(g, 'str', '111')

@app.route("/")
def helloworld():
    return "Hello Flask World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True) # 127.0.0.1 == localhost

