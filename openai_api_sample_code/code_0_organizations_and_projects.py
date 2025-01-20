# Organizations and projects (optional)

import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
organization_key = 'org-oCdLdxm1UFDyjxEUcfi29KLo'
project_key = '$PROJECT_ID'


def set_organization_and_projects(organization, project):
    # APIリクエストに使用する組織とプロジェクトを指定する。
    client = OpenAI(api_key='<KEY>')
    client = OpenAI(
        organization=organization_key,
        project=project_key,
    )
