from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import build_graph, aggregate_data, filter_data
from google_ads_service import authenticate, fetch_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Placeholder for Google Ads API client
ads_client = None

@app.route('/api/authenticate', methods=['POST'])
def authenticate_google_ads():
    global ads_client
    authorization_code = request.json.get('code')
    ads_client = authenticate(authorization_code)
    if ads_client:
        return jsonify({'message': 'Authentication successful'})
    else:
        return jsonify({'error': 'Authentication failed'}), 401

@app.route('/api/data', methods=['GET'])
def get_data():
    if not ads_client:
        return jsonify({'error': 'Not authenticated'}), 401

    customer_id = request.args.get('customerId')
    campaign_status = request.args.get('campaignStatus')
    # Note: No geography filter for MVP as per requirements

    try:
        raw_data = fetch_data(ads_client, customer_id, campaign_status)
        graph = build_graph(raw_data)

        # Aggregate data for the top level (initial view)
        aggregated_data = aggregate_data(graph)

        return jsonify(aggregated_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/drilldown', methods=['GET'])
def drill_down():
    if not ads_client:
        return jsonify({'error': 'Not authenticated'}), 401

    node_id = request.args.get('nodeId') # Campaign or Match Type ID
    try:
        # Fetch the whole graph first
        customer_id = request.args.get('customerId')
        campaign_status = request.args.get('campaignStatus')
        raw_data = fetch_data(ads_client, customer_id, campaign_status)
        graph = build_graph(raw_data)

        # Use the graph for drilldown
        filtered_data = filter_data(graph, node_id)
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)