import json
import re as regex
import resume.constants as const
from resume.header import Header
from resume.education import Education
from resume.skills import Skills
from resume.experience import Experience
from resume.projects import Projects 


class ResumeBuilder:
    """
    Generates the typst code required to build the resume
    """

    def __init__(self, config_path: str = "config.json"):
        with open(config_path, "r") as file:
            self.config = json.load(file)
            self.__parse_settings()
            self.__build_parts()

        file.close()

    def __parse_settings(self):
        self.part_order = ["header", 
                           "education", 
                           "skills", 
                           "experience", 
                           "projects"]
        self.font_size = 11
        self.margins = 1 # cm

        if "settings" in self.config:
            if "margins" in self.config["settings"]:
                self.margins = self.config["settings"]["margins"]
            if "font_size" in self.config["settings"]:
                self.font_size = int(self.config["settings"]["font_size"])
            if "part_order" in self.config["settings"]:
                self.part_order = self.config["settings"]["part_order"]
            if ("link" not in self.config["settings"] 
                or self.config["settings"]["link"]):
                self.__add_links(self.config)

    def __add_links(self, df):
        for section_key in df.keys():
            subsection = df[section_key]
            if isinstance(subsection, str) and "http" in subsection:
                df[section_key] = self.__replace_link(subsection)
            elif isinstance(subsection, dict):
                self.__add_links(subsection)
            elif isinstance(subsection, list):
                for index, entry in enumerate(subsection):
                    if isinstance(entry, dict):
                        self.__add_links(entry)
                    elif "http" in entry:
                        subsection[index] = self.__replace_link(entry)

    def __replace_link(self, text):
        match = r"https?:\/\/(.*)"
        fmt = regex.search(match, text).group(1)
        return f"""#link("{text}")[{fmt}]"""

    def __build_parts(self):
        self.resume_parts = []
        self.resume_part_map = {
            "header": Header,
            "education": Education,
            "skills": Skills,
            "experience": Experience,
            "projects": Projects
        }

        for part_name in self.part_order:
            if (part_name in self.config 
                and part_name in self.resume_part_map):
                resp = self.config[part_name]
                resume_part = self.resume_part_map[part_name](resp)
                self.resume_parts.append(resume_part)

    def build_resume(self):
        typst_str = f"""
        #set page(margin: {self.margins}cm)
        #set text(font: "Charter", size: {self.font_size}pt)
        #set par(leading: 0.5em, spacing: 0.5em)
        #set block(spacing: 0.5em)
        #show link: underline.with(stroke: 0.5pt, offset: 1.5pt)
        """
        for resume_part in self.resume_parts:
            typst_str += resume_part.to_typst_str()
        
        return typst_str
