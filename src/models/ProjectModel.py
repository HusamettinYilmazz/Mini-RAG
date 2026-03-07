from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump())
        project.id = result.inserted_id

        return project

    async def get_or_create_project(self, project_id: str):
        
        record = await self.collection.find_one({"project_id": project_id})

        if not record:
            project = await self.create_project(Project(project_id=project_id))
            return project
        
        return Project(**record)

    async def get_all_projects(self, page: int=1, page_size: int=20):
        total_projects = await self.collection.count_documents({})

        total_pages = total_projects // page_size
        if total_projects % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip(page * page_size - page_size).limit(page_size)

        projects = []
        async for record in cursor:
            projects.append(Project(**record))

        return projects, total_pages
