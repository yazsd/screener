from flask import Flask, render_template, request, flash, redirect, jsonify, json, send_file

app = Flask(__name__)
app.secret_key = b'somelongrandomstring'

def get_logs(fn):
    with open(fn,'rb') as f:
        val = f.read()
    sp = val.decode('ascii').split('\n')[:-1]
    if ((len(sp) > 10) and ('sig' in fn)):
        return sp[-10:]
    if(('pos' in fn) and (len(sp) > 80)):
        return sp[-80:]
    return sp

@app.route('/s')
def sig_logs():
    sig_log_fn = '/home/ubuntu/TRDR/zigzag-hk/sig-log.txt'
    sig_logs = get_logs(sig_log_fn)
    return render_template('log.html', sig_logs=sig_logs, tit='Sig')

@app.route('/p')
def pos_logs():
    pos_log_fn = '/home/ubuntu/TRDR/zigzag-hk/pos-log.txt'
    pos_logs = get_logs(pos_log_fn)
    return render_template('log.html', sig_logs=pos_logs, tit='Pos')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
    # app.run(debug=True)
