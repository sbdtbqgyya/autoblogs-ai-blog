# -*- coding: utf-8 -*-

import os
import pathlib
import getpass
from dotenv import load_dotenv

from autoblogs.config.default import homepage
from autoblogs.model.dataflows import AIModel, AIRequest
from autoblogs.manager.client import ClientManager
from autoblogs.manager.content import ContentManager


def welcome():
    asciiart_path = pathlib.Path(__file__).parent / "static" / "ascii.graffiti.txt"

    try:
        asciiart = open(asciiart_path, "r", encoding="utf-8").read()
    except:
        asciiart = "=== AutoBlogs CLI ==="

    print(f"\033[96m{asciiart}\033[0m\n")

    print(
        f"Welcome {getpass.getuser()} to AutoBlogs CLI!\n"
        f"Homepage: {homepage}\n"
    )


def launch():
    welcome()
    load_dotenv()

    # ===== 环境变量 =====
    provider = os.getenv("LLM_PROVIDER", "openai")
    modelname = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")
    apikey = os.getenv("LLM_MODEL_APIKEY")
    base_url = os.getenv("LLM_API_BASE_URL")

    outdir = os.getenv("CONTENT_OUTPUT_DIR", "output")
    
    # 🔧 【修复 1】：防御性代码。如果环境变量未配置模板，给一个默认模板名，防止 Jinja2 抛出 NoneType 错误
    promptfile = os.getenv("AGENT_PROMPT_CONTEXT")
    if not promptfile:
        promptfile = "default.md"

    # ===== client & content =====
    client = ClientManager(
        provider=provider,
        modelname=modelname,
        apikey=apikey,
        base_url=base_url
    )

    content = ContentManager(
        outdir=outdir,
        context=promptfile
    )

    method = client.client

    # ===== 用户输入 =====
    # 🔧 【修复 2】：去掉 input 内的提示文字。因为 auto_generate.py 是通过管道批量喂入数据的，
    # 带有提示文字会导致标准输出混乱并被捕捉到日志里。
    topic = input()
    prompt = input()
    keywords = input()

    context = content.render(
        topic=topic,
        tags=keywords,
        is_refinement=False,
        word_count_min=800,
        word_count_max=1200,
        n_sub_sections=4,
        using_claude=(client.provider.name == "CLAUDE"),
    )

    request = AIRequest(
        topic=topic,
        prompt=prompt,
        context=context
    )

    model = AIModel(
        provider=client.provider,
        useModel=modelname,
        max_tokens=int(os.getenv("MAX_TOKENS", 1000)),
        temperature=float(os.getenv("TEMPERATURE", 0.7))
    )

    # ===== 调用 AI =====
    response = method(
        model=model,
        request=request,
        apikey=apikey,
        base_url=base_url
    )

    # ===== 保存文件 =====
    # 🔧 【修复 3】：同样去掉保存文件时的提示文字，保持管道通信纯净
    outfile = input()

    os.makedirs(outdir, exist_ok=True)

    content.writefile(
        content=response.raw_response,
        filename=os.path.join(outdir, outfile)
    )

    print("\n✅ Done! File saved to:", os.path.join(outdir, outfile))

    return response


# =========================
# 🚀 程序入口
# =========================
if __name__ == "__main__":
    launch()