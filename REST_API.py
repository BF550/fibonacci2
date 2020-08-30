from flask import Flask, jsonify, request
from flask_caching import Cache
import sequences as seq

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# creating a Flask app
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/fib/<int:num>', methods=['GET'])
def fib(num):
    if request.method == 'GET':
        if isinstance(num, int) and num >= 2:
            # Check if we have the result for this num cached
            subset_str = cache.get(str(num))
            if subset_str:
                app.logger.info('returning cached result for %s', num)
                return subset_str
            else:
                # check if we have already have cached a fibonacci sequence to start with
                sequence = cache.get("fib_sequence")
                if sequence:
                    app.logger.info('%s was cached for sequence', sequence)
                else:
                    sequence = seq.FibonacciSortedSequence()  # [2, 3]
                sequence.get_subsequence(num)
                cache.set("fib_sequence", sequence)
                # Cache the subsets for the target
                # subsets_json = jsonify({'subsets': sequence.get_subsets(num)})
                subset_str = '%s\n' % str(sequence.get_subsets(num))
                cache.set(str(num), subset_str)
                return subset_str
        else:
            raise InvalidUsage('%s is not an integer greater or equal 2' % num, status_code=400)


@app.route('/health', methods=['GET'])
def health_check():
    if cache:
        # TODO: run unit tests and jsonify the results
        health = {'cache_conf': config,
                  'unit_test_results': "We passed the unit tests or we don't"
                  }
    return jsonify(health)


# driver function
if __name__ == '__main__':
    app.run(debug=True)



