"""
Adapted from: https://github.com/PatWalters/interactive_plots
"""
import base64
from io import BytesIO
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
# from rdkit import Chem
# from rdkit.Chem.Draw import MolsToGridImage

from mol_view import get_radius_size, process_data

df, df_A, df_B = process_data(path_to_df="data/tnse_combined.csv")
size_A = get_radius_size(path_to_df="data/ae_acids.csv")
size_B = get_radius_size(path_to_df="data/ae_bases.csv")

label_A = "Novartis Acids"
label_B = "Novartis Bases"

graph_component = dcc.Graph(
    id='tsne',
    config={'displayModeBar': False},
    figure={
        'data': [
            go.Scattergl(
                x=df_A.X,
                y=df_A.Y,
                mode='markers',
                opacity=0.9,
                marker={
                    'color': 'red',
                    'size': size_A,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=label_A,
            ),
            go.Scattergl(
                x=df_B.X,
                y=df_B.Y,
                mode='markers',
                opacity=0.9,
                marker= {
                    'color': 'darkblue',
                    'size': size_B,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=label_B,
            ),
        ],
        'layout': go.Layout(
            height=400,
            xaxis={'title': 'X'},
            yaxis={'title': 'Y'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            dragmode='select'
        )
    }
)

image_component = html.Img(id="structure-image")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([graph_component]),
    html.Div([image_component])
])


@app.callback( Output('structure-image', 'src'), [Input('tsne', 'selectedData')])
def display_selected_data(selectedData):
    max_structs = 100
    structs_per_row = 4
    empty_plot = "data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA="

    if selectedData:
        if len(selectedData['points']) == 0:
            return empty_plot

        match_idx = [x['pointIndex'] for x in selectedData['points']]

        match_df = df.loc[match_idx]

        smiles_list = list(match_df.SMILES)

        pka_list = list(match_df.pKa)
        source_list = list(match_df.type)
        compound_type_list = list(match_df["Compound Annotation"])

        # mol_list = [Chem.MolFromSmiles(x) for x in smiles_list]
        # name_list = [f"Exp. pKa={pka} | {type} " for (pka, source, type, smi) in
        #              zip(pka_list, source_list, compound_type_list, smiles_list)]
        #
        # img = MolsToGridImage(mol_list[0:max_structs], molsPerRow=structs_per_row, legends=name_list)
        buffered = BytesIO()
        # img.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue())
        src_str = 'data:image/png;base64,{}'.format(encoded_image.decode())
    else:
        return empty_plot

    return src_str

if __name__ == '__main__':
    import socket

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    app.run_server(debug=True, host=IPAddr)
