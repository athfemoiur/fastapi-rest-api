from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException
from starlette import status
from typing import List

from starlette.responses import Response

from mongodb import db
from models.product import Product, ProductCreate, BaseProduct
from serializer import serialize_list, serialize_dict

from bson import ObjectId

product = APIRouter(prefix='/products')


@product.get('/', response_model=List[Product])
async def get_all_products():
    products = list()
    cursor = db.product.find()
    async for document in cursor:
        products.append(document)
    return serialize_list(products)


@product.post('/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_user(product: ProductCreate):
    product_dict = dict(product)
    if await db.user.find_one({'name': product_dict['name']}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='A product with this name already exists')
    created_product = await db.product.insert_one(product_dict)
    created_product = await db.product.find_one({'_id': created_product.inserted_id})
    return serialize_dict(created_product)


@product.get('/{id}/', response_model=Product)
async def get_product(product_id: str):
    try:
        product_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='id is not valid')
    product = await db.product.find_one({'_id': product_id})
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return serialize_dict(product)


@product.delete('/{id}/')
async def delete_product(product_id: str):
    try:
        product_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='id is not valid')
    result = await db.product.delete_one({'_id': product_id})
    if not result.deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@product.put('/{id}/', response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    try:
        product_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='id is not valid')
    await db.product.find_one_and_update({'_id': product_id}, {'$set': dict(product)})
    updated_product = await db.product.find_one({'_id': product_id})
    return serialize_dict(updated_product)


@product.patch('/{id}/', response_model=Product)
async def update_product(product_id: str, product: BaseProduct):
    try:
        product_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='id is not valid')
    update_data = product.dict(exclude_unset=True)
    await db.product.find_one_and_update({'_id': product_id}, {'$set': dict(update_data)})
    updated_product = await db.product.find_one({'_id': product_id})
    return serialize_dict(updated_product)
