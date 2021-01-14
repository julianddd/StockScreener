from modules import instrumentData, instrumentIDs

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/symbols')
def symbols():
    exchange = str(request.args.get('exchange'))
    return jsonify(instrumentIDs.InstrumentIds.getInstrumentIds('', exchange))

@app.route('/instrument')
def instrument():
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')
    ti = request.args.get('ti')
    interval = request.args.get('interval')

    if ti is None:
        return instrumentData.InstrumentData.getInstrumentTimeSeries('', symbol, exchange)
    return instrumentData.InstrumentData.getInstrumentTechnical(instrumentData.InstrumentData, symbol, exchange, ti, interval)