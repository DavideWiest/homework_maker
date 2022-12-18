import os
from datetime import datetime, timedelta
import uuid

import pdfkit

from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("doc_creator"),
    autoescape=select_autoescape()
)

pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#imgkit_config = imgkit.configuration(wkthmltoimg=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

class DocCreator:
    def __init__(self, base_params):
        self.base_params = base_params

        self.homework_template = env.get_template("homework.html")
        self.addon_options = {
            # "footer_right": env.get_template("footer_right.html"),
            # "header_right": env.get_template("header_right.html")
        }

    def get_options(self, options):
        options["margin-bottom"] = "10mm"
        options["margin-top"] = "10mm"
        options["--enable-local-file-access"] = None
        
        return options

    def remove_tempfiles(self, _options):
        if "--header-html" in _options:
            os.remove(_options["--header-html"])
        if "--footer-html" in _options:
            os.remove(_options["--footer-html"])

    def pdf_from_file(self, filename: str, output_path: str, options: dict={}):
        _options=self.get_options(options)
        pdfkit.from_file(filename, output_path, options=_options, configuration=pdfkit_config, css=[os.path.abspath("styles/styles.css")])
        self.remove_tempfiles(_options)

    def pdf_from_str(self, html: str, output_path: str, options: dict={}):
        _options=self.get_options(options)
        pdfkit.from_string(html, output_path, options=_options, configuration=pdfkit_config, css=[os.path.abspath("styles/styles.css")])
        self.remove_tempfiles(_options)

    def render_addons(self, addon_option: str, overwrite_base_params: dict = {}):
        _base_params=self.base_params
        if overwrite_base_params != {}:
            for overwrite_name, overwrite_datapoint in overwrite_base_params.items():
                _base_params[overwrite_name] = overwrite_datapoint

        _contents=self.base_params["header"] if addon_option.startswith("header") else self.base_params["footer"]
        _contents = _contents.split("{img:")
        addonfiles = [f for f in os.listdir("dc/static/addonfiles/") if os.path.isfile(os.path.join("dc/static/addonfiles/", f))]

        getimg = lambda filename: "<img src='" + os.path.join("dc/static/addonfiles/", filename) + "' style='width: 1.3rem; vertical-align: center; display: inline-block; max-width: 100%; height: auto; margin: 0 0.4rem;'>"
        if len(_contents) > 1:
            for index in range(len(_contents)-1):
                parse_list = []
                for x in addonfiles:
                    if _contents[index+1].startswith(x + "}"):
                        parse_list.append(x)
                #any([_contents[index+1].startswith(x + "}") for x in addonfiles])
                if parse_list != []:
                    for i in parse_list:
                        _contents[index+1] = getimg(i).join(_contents[index+1].split(i+"}"))

        _contents="".join(_contents)
        addon_rendered = self.addon_options[addon_option].render(
            contents=_contents
        )

        temp_addon_file=os.path.abspath("dc/tempfiles") + f"/{uuid.uuid4().hex}.html"
        with open(temp_addon_file, "w", encoding="utf-8") as f:
            f.write(addon_rendered)
        
        return temp_addon_file

    def render_homework(self, _params: dict):
        
        base_params = self.base_params

        template_rendered = self.homework_template.render(
            title=_params.get("title", "Hausaufgaben"),
            tasks=_params["tasks"],
            info=_params.get("info", ""),
            date=datetime.now().strftime("%d.%m.%Y"),
            itemlist=list(_params["tasks"]),
            base_params=base_params
        )

        return template_rendered

if __name__ == '__main__':
    dc = DocCreator({})

    params = {
        "title": "Hausaufgaben",
        "info": "Von Davide Wiest",
        "tasks": [
            ["Frage", "Antwort"],
            ["Frage", "Antwort"]
        ]
    }

    homework_done = dc.render_homework(params)
    try:
        dc.pdf_from_str(homework_done, "homework_done.pdf")
    except OSError:
        pass