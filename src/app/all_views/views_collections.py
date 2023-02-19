from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework import status
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from app.models import CustomCollection, Token, MAX_LENGTH_CUSTOMCOLLECTION_NAME, MAX_LENGTH_TOKEN_NAME
import json
import datetime


def serialize_token(t):
    return {
        'id': t.id,
        'tokenId': t.token_id,
        'name': t.name,
        'image': t.image_src
    }


def serialize_collection(collection, add_tokens=False):
    ret = model_to_dict(collection)
    ret['last_updated'] = str(ret['last_updated'])
    ret['date_added'] = str(ret['date_added'])
    if add_tokens:
        ret['tokens'] = [serialize_token(
            t) for t in Token.objects.filter(collection=collection)]
    return ret


def get_token_data_from_dict(token):
    return token.get('tokenId'), token.get('image'), token.get('name')


def get_token_error_message(token):
    token_id, token_image_src, token_name = get_token_data_from_dict(token)
    if not token_id or not isinstance(token_id, str):
        return 'Token id must be string'
    if not token_image_src or not isinstance(token_image_src, str):
        return 'Token image src must be string'
    if (token_name is not None) and (not isinstance(token_name, str)):
        return 'Token name must be string'
    return None


def save_collection(request, collection, success_status):
    errors = []
    collection_name = request.data.get("collectionName", "")
    tokens = request.data.get('tokensList', [])
    if collection_name == "" or (not isinstance(collection_name, str)):
        errors.append("Collection name is required")
    elif len(collection_name) > MAX_LENGTH_CUSTOMCOLLECTION_NAME:
        errors.append("Collection name length must be at most {} characters".format(
            MAX_LENGTH_CUSTOMCOLLECTION_NAME
        ))
    if not tokens or (not isinstance(tokens, list)):
        errors.append('Tokens must be a non-empty list')
    else:
        for token in tokens:
            error_msg = get_token_error_message(token)
            if error_msg:
                errors.append(error_msg)
                break
    if len(errors) > 0:
        return HttpResponse(json.dumps(
            {
                "errors": errors,
                "show_errors": True
            }), status=status.HTTP_400_BAD_REQUEST)
    all_errors = []
    try:
        collection.name = collection_name
        collection.token_count = len(tokens)
        collection.user = request.user
        collection.last_updated = datetime.datetime.now()
        if not collection.id:
            collection.date_added = datetime.datetime.now()
        collection.save()
        token_ids_set = {t['tokenId'] for t in tokens}
        for existing_token in Token.objects.filter(collection=collection):
            if existing_token.token_id not in token_ids_set:
                existing_token.delete()
        for idx, token in enumerate(tokens):
            token_id, token_image_src, token_name = get_token_data_from_dict(
                token)
            try:
                token_obj = Token.objects.get(
                    collection=collection, token_id=token_id)
            except ObjectDoesNotExist:
                token_obj = Token()
            token_obj.collection = collection
            token_obj.token_id = token_id
            token_obj.image_src = token_image_src
            token_obj.name = token_name
            token_obj.index_in_collection = idx
            token_obj.save()
    except Exception as e:
        return HttpResponse(json.dumps(
            {
                "errors": all_errors or [str(e)],
                "show_errors": len(all_errors) > 0
            }), status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(json.dumps({"data": serialize_collection(collection)}), status=success_status)


@ api_view(['GET', 'POST'])
def collections(request):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        collections = CustomCollection.objects.filter(user=request.user)
        collections = [serialize_collection(
            collection) for collection in collections]
        return HttpResponse(json.dumps({"data": {
            'collections': collections,
        }}), status=status.HTTP_200_OK)

    if request.method == "POST":
        collection = CustomCollection()
        return save_collection(request, collection, status.HTTP_201_CREATED)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)


@ api_view(['GET', 'DELETE', 'PUT'])
def collection(request, collection_id):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    try:
        collection = CustomCollection.objects.get(
            pk=collection_id, user=request.user)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"detail": "Not found"}), status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return HttpResponse(json.dumps({"data": serialize_collection(collection, add_tokens=True)}), status=status.HTTP_200_OK)

    if request.method == "PUT":
        return save_collection(request, collection, status.HTTP_200_OK)

    if request.method == "DELETE":
        collection.delete()
        return HttpResponse(json.dumps({"detail": "deleted"}), status=status.HTTP_410_GONE)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)
