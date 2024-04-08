def build_joblist_markmap(job_list: dict[str, list[str]]) -> str:
    data = """
    ---
    markmap:
    colorFreezeLevel: 2
    ---

    #

    """

    for job, tech_list in job_list.items():
        data += f"## {job}" + "\n"
        for tech in tech_list:
            data += f"### {tech}" + "\n"
    return data
