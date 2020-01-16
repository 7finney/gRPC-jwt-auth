
"""Interceptor that ensures a specific header is present."""

import grpc


def _unary_unary_rpc_terminator(code, details):

    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class RequestHeaderValidatorInterceptor(grpc.ServerInterceptor):

    def __init__(self, code, details):
        self._terminator = _unary_unary_rpc_terminator(code, details)

    def intercept_service(self, continuation, handler_call_details):
        print("handler call details: ", handler_call_details.invocation_metadata)
        authToken = handler_call_details.invocation_metadata[0][1]
        print("authToken: ", authToken)
        if (len(authToken) > 0):
            return continuation(handler_call_details)
        else:
            return self._terminator