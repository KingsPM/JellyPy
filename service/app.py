#!/usr/bin/env python
from flask import Flask, request, jsonify
import re
from pyCIPAPI.interpretation_requests import get_interpretation_request_json
from pyCIPAPI.summary_findings import create_cr, post_cr, num_existing_reports, get_ref_db_versions, \
    gel_software_versions, number_tiered_variants
import jwt
from jwt.exceptions import InvalidTokenError, DecodeError, ExpiredSignatureError

app = Flask(__name__)

# root
@app.route('/')
def index():
    return "CIPAPI gateway service"


@app.route('/api/close_case/<_irvn>', methods=['POST'])
def api_message(_irvn):

    # check format of id request:
    if not bool(re.match(r"^\d+-\d+$", _irvn)):
        return jsonify('Invalid request id & request_version: %s' % _irvn)
    else:
        ir_id, ir_version = _irvn.split('-')

    # Get IR data
    ir_json_v6 = get_interpretation_request_json(ir_id, ir_version,
                                                 token=request.headers['auth_token'],
                                                 reports_v6=True,
                                                 testing_on=request.json['testing_on'])

    # Check that an clinical report hasn't already been submitted
    if num_existing_reports(ir_json_v6):
        return jsonify('%s existing clinical reports detected for interpretation request: %s'
                       % (num_existing_reports(ir_json_v6), _irvn))

    # Check there really aren't any tier 1 or 2 variants for this IR
    number_variants =  number_tiered_variants(ir_json_v6)
    if number_variants['T1'] != 0 or number_variants['T2'] != 0:
        return jsonify('Cannot automatically close case as there are tier 1 and/or tier 2 variants present: %s'
                       % number_variants)

    # Get authenticated user from decoded token
    try:
        decoded_token = jwt.decode(request.headers['auth_token'], verify=False)
        username = decoded_token['username']
    except (InvalidTokenError, DecodeError, ExpiredSignatureError, KeyError) as e:
        raise jsonify(e)
    except:
        raise

    # Create clinical report object
    cr = create_cr(interpretationRequestId=ir_id,
                   interpretationRequestVersion=int(ir_version),
                   reportingDate=request.json['reportingDate'],
                   user=username,
                   referenceDatabasesVersions=get_ref_db_versions(ir_json_v6),
                   softwareVersions=gel_software_versions(ir_json_v6),
                   genomicInterpretation="No tier 1 or 2 variants detected"
                   )

    # Push clinical report to CIP-API
    response = post_cr(clinical_report=cr, ir_json_v6=ir_json_v6,
                       testing_on=request.json['testing_on'],
                       token=request.headers['auth_token'])

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
