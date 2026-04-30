# -*- coding: utf-8 -*-

import time
from uuid import uuid4 as UUIDx

import openai

from autoblogs.model.dataflows import AIResponse


def generateOpenAI(model, request, apikey, base_url=None):
    """
    OpenAI SDK wrapper for AutoBlogs.

    Sends chat completion request and returns standardized AIResponse.
    """

    start = time.monotonic()

    # =========================
    # 设置 API Key
    # =========================
    client = openai.OpenAI(
        api_key=apikey,
        base_url=base_url
    )

    # =========================
    # 构造 messages
    # =========================
    messages = [
        {
            "role": "user",
            "content": request.prompt + "\n\n" + (request.context or "")
        }
    ]

    try:
        # =========================
        # 调用 OpenAI
        # =========================
        response = client.chat.completions.create(
            model=model.useModel,
            messages=messages,
            max_tokens=int(model.max_tokens) if model.max_tokens else 1000,
            temperature=float(model.temperature) if model.temperature else 0.7
        )

        raw_response = (
            response.choices[0].message.content
            if response.choices else "No response"
        )

        return AIResponse(
            request_id=request.request_id or str(UUIDx()),
            raw_response=raw_response,
            in_tokens=getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
            out_tokens=getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
            latency=time.monotonic() - start
        )

    except Exception as e:
        return AIResponse(
            request_id=request.request_id or str(UUIDx()),
            raw_response=f"ERROR: {str(e)}",
            in_tokens=0,
            out_tokens=0,
            latency=time.monotonic() - start
        )
