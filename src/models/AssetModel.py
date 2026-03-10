from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums import DataBaseEnum
from bson.objectid import ObjectId


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        await instance.init_indexes()

        return instance

    async def init_indexes(self):
        indexes = Asset.get_indexes()

        for idx in indexes:
            await self.collection.create_index(
                idx["key"],
                name= idx["name"],
                unique=idx["unique"]
            )

    async def insert_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id

        return asset
    
    async def get_asset(self, project_id: str, asset_name: str):
        record = await self.collection.find_one({
            "asset_project_id": project_id,
            "asset_name": asset_name
        })

        if not record:
            return None
        
        return Asset(**record)

    async def get_all_project_assets(self, project_id: str, asset_type: str=None):
        if not asset_type:
            records = await self.collection.find({
                "asset_project_id": ObjectId(project_id)
                }).to_list(length=None)

        records = await self.collection.find({
                "asset_project_id": ObjectId(project_id),
                "asset_type": asset_type
                }).to_list(length=None)

        return [
            Asset(**record)
            for record in records
            ]