#!/usr/bin/env python
from flask import Flask, request, jsonify
import re
from datetime import datetime
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
        return jsonify({'error': 'Invalid request id & request_version: %s' % _irvn}), 400
    else:
        ir_id, ir_version = _irvn.split('-')

    # Check required header data
    try:
        auth_token = request.headers['x-passtoken-cipapi']
    except KeyError:
        return jsonify({'error': 'Missing CIP API authorisation token'}), 401
    except:
        raise

    # Check if reportingDate provided
    try:
        reportingDate = request.json['reportingDate']
    except KeyError:
        reportingDate = datetime.today().strftime("%Y-%m-%d")
    except:
        raise

    # Get authenticated user from decoded token
    try:
        decoded_token = jwt.decode(auth_token, verify=False)
        username = decoded_token['username']
    except (InvalidTokenError, DecodeError, ExpiredSignatureError, KeyError) as e:
        return jsonify({'error': 'JWT token decode error:' + str(e)}), 401
    except:
        raise

    # Get testing_on status (if present)
    try:
        testing_on = request.json['testing_on']
    except KeyError:
        testing_on = False
    except:
        raise

    # Get IR data
    try:
        ir_json_v6 = get_interpretation_request_json(ir_id, ir_version,
                                                     token=auth_token,
                                                     reports_v6=True,
                                                     testing_on=testing_on)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Check that an clinical report hasn't already been submitted
    try:
        if num_existing_reports(ir_json_v6):
            return jsonify({'error': '{} existing clinical reports detected for interpretation request: {}'
                           .format(num_existing_reports(ir_json_v6), _irvn)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Check there genuinely aren't any tier 1 or 2 variants for this IR
    try:
        number_variants = number_tiered_variants(ir_json_v6)
        if number_variants['T1'] != 0 or number_variants['T2'] != 0:
            return jsonify({'error': 'Cannot close case as there are tier 1 and/or tier 2 variants present: {}'
                           .format(number_variants)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Create clinical report object
    try:
        cr = create_cr(interpretationRequestId=ir_id,
                       interpretationRequestVersion=int(ir_version),
                       reportingDate=reportingDate,
                       user=username,
                       referenceDatabasesVersions=get_ref_db_versions(ir_json_v6),
                       softwareVersions=gel_software_versions(ir_json_v6),
                       genomicInterpretation="No tier 1 or 2 variants detected"
                       )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Push clinical report to CIP-API
    try:
        response = post_cr(clinical_report=cr, ir_json_v6=ir_json_v6,
                           testing_on=testing_on,
                           token=auth_token)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
