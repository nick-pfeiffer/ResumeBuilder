from resume.resume_part import ResumePart
import resume.constants as const
import resume.utils as utils


class Education(ResumePart):
    def __init__(self, config_map):
        self.section_map = {}
        for index, section in enumerate(config_map):
            assert "school" in section
            assert "graduation" in section
            assert "degree" in section

            self.section_map[index] = {
                "school": section["school"],
                "graduation": section["graduation"],
                "degree": section["degree"],
                "gpa": "" if "gpa" not in section else section["gpa"],
                "honors": ([] if "honors" not in section
                                else section["honors"]),
                "courses": ([] if "courses" not in section 
                                else section["courses"]),
            }

    def to_typst_str(self) -> str:
        content = ""
        for index in range(0, len(self.section_map)):
            items = self.section_map[index]
            content += f"""#grid(
                columns: (6fr, 1fr, 3fr),
                [
                    #text(weight: "bold")[{items["school"]}] – {items["degree"]}
                ],
                text()[],
                text()[
                    #set align(right)
                    {items["graduation"]}
                ],
            )
            """
            lines = ""
            details = []
            if items["gpa"]:
                details.append(f"""#text(weight: "bold")[GPA:] {items["gpa"]}""")
            details.extend(items["honors"])
            if len(details) > 0:
                lines += " | ".join(details) + " \\ \n"
            if len(items["courses"]) > 0:
                for course_map in items["courses"]:
                    name = course_map["name"]
                    classes = course_map["items"]
                    classes_str = ", ".join(classes)
                    lines += f"""#text(weight: "bold")[{name}:]\n"""
                    lines += f"""#text()[{classes_str}] \\ \n"""
            content += lines

        section = f"""
        {utils.create_heading("Education")}
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
