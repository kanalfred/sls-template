import os
import json
import time
import inspect
from slstpl.util.logger import logger


def http_response(handler_func):
    def handler_wrapper(event, context, **kwargs):
        code = 200
        reason = 0
        error_msg = None
        try:
            result = handler_func(event, context, **kwargs)
        except (RequestError, HandlerError) as error:
            logger.exception(error.message)
            code = error.code
            reason = error.reason
            error_msg = error.message
        except Exception as error:
            logger.exception('Unexpected Error')
            code = 500
            error_msg = repr(error)

        if error_msg is None:
            body = result

        else:
            if 'pathParameters' in event:
                logger.error("Function called with parameters: %s" % event['pathParameters'])
            if 'body' in event:
                logger.error("Function called with body: %s" % event['body'])
            body = {'error': {'code': code, 'reason': reason, 'message': error_msg}}

        if isinstance(body, dict):
            result = json.dumps(body)
        else:
            result = body
        return {"statusCode": code, "body": result + "\n"}

    return handler_wrapper


def func_timer(handler_func):
    def handler_wrapper(*args):
        func_name = inspect.stack()[1][3]
        logger.info("FUNC {} start params: {}".format(func_name, str(args)))
        get_start = time.time()
        result = handler_func(*args)
        get_end = time.time()
        logger.info("FUNC {} end time: ".format(func_name, get_end - get_start))
        return result
    return handler_wrapper
