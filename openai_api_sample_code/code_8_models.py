# models
# modelations create_moderation
from openai import OpenAI

client = OpenAI()

model_retrieve_4o_mini = "gpt-4o-mini"
model_retrieve_35_turbo_instruct = "gpt-3.5-turbo-instruct"


def list_models():
    response = client.models.list()
    return response


def models_retrieve(model_name=model_retrieve_4o_mini):
    # 特定のテキスト入力が潜在的に有害であるかどうかを表します。
    """
    Retrieves a model instance, providing basic information about the model
    such as the owner and permissions.
    モデル インスタンスを取得し、所有者や権限などのモデルに関する基本情報を提供します。
    """
    return client.models.retrieve(model_name)


def delete_models(model_name=model_retrieve_4o_mini):
    """
    - Delete a fine-tuned model. You must have the Owner role in your organization to delete a model.
    - 微調整されたモデルを削除します。モデルを削除するには、組織内で所有者の役割を持っている必要があります。
    """
    response = client.models.delete("ft:gpt-4o-mini:acemeco:suffix:abc123")
    return response


def delete_fine_tuning_model(model_string):
    # model_delete_a_fine_tuned_model
    # model_string = "ft:gpt-4o-mini:acemeco:suffix:abc123"
    response = client.models.delete(model_string)
    return response


"""
response = {
  "id": "ft:gpt-4o-mini:acemeco:suffix:abc123",
  "object": "model",
  "deleted": true
}

"""
pass
# response
"""
response = {
  "id": "gpt-4o-mini",
  "object": "model",
  "created": 1686935002,
  "owned_by": "system"
}
"""
# list models
"""
{
  "object": "list",
  "data": [
    {
      "id": "model-id-0",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    },
    {
      "id": "model-id-1",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner",
    },
    {
      "id": "model-id-2",
      "object": "model",
      "created": 1686935002,
      "owned_by": "openai"
    },
  ],
  "object": "list"
}
"""
