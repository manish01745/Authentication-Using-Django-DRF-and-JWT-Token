# from rest_framework import renderers
# import json

# class UserRenderer(renderers.JSONRenderer):
#     charset ='utf-8'
#     def render(self,data,accepted_media_type=None,renderer_context=None):
#         response =''
#         if 'ErrorDetail' in str(data):
#             response =json.dumps({'error':data})
#         else:
#             response=json.dumps(data)
#         return response


from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            # Handle error response
            response = json.dumps({'error': data})
        else:
            # Convert non-JSON serializable objects (like sets) to lists
            data = self.handle_non_serializable_data(data)
            response = json.dumps(data)

        return response

    def handle_non_serializable_data(self, data):
        # Convert sets to lists to make them JSON serializable
        if isinstance(data, set):
            return list(data)
        elif isinstance(data, dict):
            # Recursively handle sets inside dictionaries
            return {key: self.handle_non_serializable_data(value) for key, value in data.items()}
        elif isinstance(data, (list, tuple)):
            # Recursively handle sets inside lists or tuples
            return [self.handle_non_serializable_data(item) for item in data]
        return data
