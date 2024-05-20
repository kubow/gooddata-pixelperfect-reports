from jinja2 import Environment, FileSystemLoader
from gooddata_pandas import GoodPandas
from pathlib import Path
from plotly.express import scatter
from weasyprint import HTML

def initial_settings(temp_folder: str="static", output_filename: str = "report"):
    return {
        "html": "template.html",
        "css": f"{temp_folder}/style.css",
        "html_final": f"{output_filename}.html",
        "logo": f"{temp_folder}/logo.svg",
        "first_visual": f"{temp_folder}/visual.png",
        "first_table": f"{temp_folder}/table.png",
        "pdf": f"{output_filename}.pdf",
    }


if __name__ == "__main__":
    settings = initial_settings()

    host = "https://navy-blue-eagle.trial.cloud.gooddata.com/"
    token = "amFrdWIudmFqZGE6TmV3Ok5Qa2d6ZTVPZElHbTVMQU1kZk1TU1R1dFpZWU4rMmNm"
    workspace_id = "gdc_demo_8233544a-ce3b-48e4-a005-cd3dabd6667f"
    table_id = '469e8936-ca67-4987-8c70-0e35be24be4d'
    vis_id = '2da13424-2a6b-4ed4-916c-9bbc002fdd1b'

    # list dataframes available within a specific workspace
    gp = GoodPandas(host, token)
    frames = gp.data_frames(workspace_id)
    
    # select visualization from a list
    vis_list = gp.sdk.visualizations.get_visualizations(workspace_id)

    # first a table generated into HTML
    table_df = frames.for_visualization(table_id)
    settings["first_table"] = table_df.to_html()

    # then a visual generated to a PNG
    vis_df = frames.for_visualization(vis_id)
    fig = scatter(vis_df)
    fig.update_layout(width=800, height=500)
    fig.write_image(settings["first_visual"], format='png')
    # re-apply absolute path on generated image
    settings["first_visual"] = str(Path.cwd().joinpath("static", "visual.png"))  

    # prepare template
    env = Environment(loader=FileSystemLoader("static"))
    template = env.get_template(settings["html"])
    # re-apply absolute path on company logo
    settings["logo"] = str(Path.cwd().joinpath("static", "logo.svg"))  

    # generate HTML report
    outputText = template.render(settings)
    with open(settings["html_final"], "w") as final:
        final.writelines(outputText)
    
    # generate PDF report
    pdf_report = HTML(string=outputText)
    pdf_report.write_pdf(
        Path.cwd().joinpath(settings["pdf"]), 
        stylesheets=[Path.cwd().joinpath(settings["css"])]
    )
