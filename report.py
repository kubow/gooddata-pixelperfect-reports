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

    host = "your_gooddata_endpoint"
    token = "api_access_token"
    workspace_id = "workspace_id"
    table_id = 'first_visual_id_table_preferably'
    vis_id = 'second_visual_id'

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
