from resume.resume_part import ResumePart
import resume.constants as const
import resume.utils as utils


class Experience(ResumePart):
    def __init__(self, config_map):
        self.entries = config_map

    def to_typst_str(self) -> str:
        content = ""
        for experience in self.entries:
            company = experience["company"]
            location = experience["location"]
            titles = experience["titles"]
            time = experience["time"]
            status = experience["status"]
            items = experience["items"]
            assert len(titles) == len(time)
            # With one title, the date sits on the company line and the
            # location on the title line; with several, the location sits on
            # the company line (blank if empty, to keep each date lined up
            # with its title).
            if len(titles) == 1:
                right = [line for line in time + [location, status] if line]
            else:
                right = [location] + time + ([status] if status else [])
            if content:
                content += f"#v({const.ENTRY_GAP})\n"
            content += f"""
            #grid(
                columns: (6fr, 1fr, 3fr),
                [
                    #text(weight: "bold")[{company}] \\
                    {"\\ \n".join(f"#emph[{title}]" for title in titles)}
                ],
                text()[],
                [
                    #set align(right)
                    {"\\ \n".join(right)}
                ],
            )
            """

            if len(items) > 0:
                content += "#list(\n"
                for item in items:
                    content += f"[{utils.convert_bold(item)}],\n"
                content += ")\n"

        section = f"""
        {utils.create_heading("Work Experience")}
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
