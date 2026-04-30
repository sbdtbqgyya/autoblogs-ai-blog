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
    promptfile = os.getenv("AGENT_PROMPT_CONTEXT")

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
    topic = input("Set Content Topic: ")
    prompt = input("Explain Prompt: ")
    keywords = input("SEO Keywords (comma separated): ")

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
    outfile = input("Output filename (e.g. post.md): ")

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
