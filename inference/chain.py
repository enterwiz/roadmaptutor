from langchain.prompts import PromptTemplate
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import JsonOutputParser

from .model import TechniquePoint
from .prompt import (
    BASE_PROMPT,
    JOB_TECH_DETAIL_PROMPT,
    JOB_TECHTREE_PROMPT,
    JOB_TASK_PROMPT,
    JOB_INTRO_PROMPT,
    JOB_PROMOTION_PROMPT,
    JOB_FAQ_PROMPT,
)

llm = Tongyi()


def gen_job_intro(job_name: str) -> str:
    job_intro_prompt = PromptTemplate.from_template(BASE_PROMPT + JOB_INTRO_PROMPT)
    chain = job_intro_prompt | llm
    return chain.invoke({"job_name": job_name, "output_format": "text"})


def gen_job_task(job_name: str) -> str:
    job_intro_prompt = PromptTemplate.from_template(BASE_PROMPT + JOB_TASK_PROMPT)
    chain = job_intro_prompt | llm
    return chain.invoke({"job_name": job_name, "output_format": "text"})


def gen_job_techtree(job_name: str) -> list[str]:
    parser = JsonOutputParser(pydantic_object=TechniquePoint)
    template = BASE_PROMPT + JOB_TECHTREE_PROMPT
    job_intro_prompt = PromptTemplate(
        template=template,
        input_variables=["job_name", "output_format"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = job_intro_prompt | llm | parser
    return chain.invoke({"job_name": job_name, "output_format": "json"})


def gen_job_techtree_v2(job_name: str) -> dict[str, list[str]]:
    parser = JsonOutputParser(pydantic_object=TechniquePoint)
    template = BASE_PROMPT + JOB_TECHTREE_PROMPT
    job_intro_prompt = PromptTemplate(
        template=template,
        input_variables=["job_name", "output_format"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = job_intro_prompt | llm | parser
    job_tech_names = chain.invoke({"job_name": job_name, "output_format": "json"})

    ret2 = {}
    for tech_name in job_tech_names:
        ret2[tech_name] = gen_tech_detail(tech_name)
    return ret2


def gen_tech_detail(tech_name: str) -> list[str]:
    parser = JsonOutputParser(pydantic_object=TechniquePoint)
    template = BASE_PROMPT + JOB_TECH_DETAIL_PROMPT
    tech_detail_prompt = PromptTemplate(
        template=template,
        input_variables=["tech_name", "output_format"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = tech_detail_prompt | llm | parser
    return chain.invoke({"tech_name": tech_name, "output_format": "json"})


def gen_job_promotion(job_name: str) -> str:
    job_intro_prompt = PromptTemplate.from_template(BASE_PROMPT + JOB_PROMOTION_PROMPT)
    chain = job_intro_prompt | llm
    return chain.invoke({"job_name": job_name, "output_format": "text"})


def gen_job_faq(job_name: str) -> str:
    job_intro_prompt = PromptTemplate.from_template(BASE_PROMPT + JOB_FAQ_PROMPT)
    chain = job_intro_prompt | llm
    return chain.invoke({"job_name": job_name, "output_format": "text"})


if __name__ == "__main__":
    ret = gen_job_techtree_v2("前端开发工程师")
    print(ret)
