# The message delta object
# メッセージのデルタ、つまりストリーミング中にメッセージ上で変更されたフィールドを表します。
pass
"""
object = {
  "id": "msg_123",
  "object": "thread.message.delta",
  "delta": {
    "content": [
      {
        "index": 0,
        "type": "text",
        "text": { "value": "Hello", "annotations": [] }
      }
    ]
  }
}
"""
pass
# The run step delta object
# API エンドポイントで参照できる実行ステップの識別子。
"""
object= {
  "id": "step_123",
  "object": "thread.run.step.delta",
  "delta": {
    "step_details": {
      "type": "tool_calls",
      "tool_calls": [
        {
          "index": 0,
          "id": "call_123",
          "type": "code_interpreter",
          "code_interpreter": { "input": "", "outputs": [] }
        }
      ]
    }
  }
}
"""
pass
# Assistant stream events
# 実行をストリーミングするときに発生するイベントを表します。
# サーバー送信イベント ストリーム内の各イベントには、次eventのdataプロパティがあります。
"""
event: thread.created
data: {"id": "thread_123", "object": "thread", ...}
"""
