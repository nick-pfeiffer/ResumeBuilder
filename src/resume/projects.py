from resume.resume_part import ResumePart
import resume.constants as const
import resume.utils as utils


class Projects(ResumePart):
    def __init__(self, config_map):
        self.entries = config_map

    def to_typst_str(self) -> str:
        content = ""
        for project in self.entries:
            name = project["name"]
            time = project["time"]
            items = project["items"]
            link = "" if "link" not in project else f"""| {project["link"]}"""
            tools = ("" if not project.get("tools")
                     else f"""| {", ".join(project["tools"])}""")

            if content:
                content += f"#v({const.ENTRY_GAP})\n"
            content += f"""
            #grid(
                columns: (1fr, auto),
                [
                     #text(weight: "bold")[{name}]
                     #text()[{tools}]
                     #text()[{link}]
                ],
                [
                    #set align(right)
                    {time}
                ],
            )
            """

            if len(items) > 0:
                content += "#list(\n"
                for item in items:
                    content += f"[{item}],\n"
                content += ")\n"

        section = f"""
        {utils.create_heading("Projects")}
        #grid(
            columns: (0.1fr, 9.8fr, 0.1fr),
            text()[],
            [
                {content}
            ],
            text()[],
        )
        """
                
        return section
