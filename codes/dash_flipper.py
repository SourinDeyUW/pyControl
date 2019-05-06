import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from time import sleep
from pymeasure.instruments.newport import ESP300

#
serial = b'37000805'
ctrl = ESP300("GPIB0::3::INSTR")

app = dash.Dash(__name__)
server = app.server
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True

# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
]
for css in external_css:
    app.css.append_css({"external_url": css})

# root_layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#
#     html.Div([
#         daq.ToggleSwitch(
#             id='toggleTheme',
#             style={
#                 'position': 'absolute',
#                 'transform': 'translate(-50%, 20%)'
#             },
#             size=25
#         ),
#     ], id="toggleDiv",
#         style={
#             'width': 'fit-content',
#             'margin': '0 auto'
#         }),
#
#     html.Div(id='page-content'),
# ])

root_layout = html.Div(
    [
        dcc.Interval(id="upon-load", interval=1000, n_intervals=0),
        dcc.Interval(id="stream", interval=5000, n_intervals=0),

        html.Div(
            [
                html.H2("Johnson AutoBox",
                        className="five columns",
                        style={'color': '#1d1d1d',
                               'margin-left': '10%',
                               'display': 'inline-block',
                               'text-align': 'center'
                               },
                        ),
                daq.StopButton(
                    id="start-stop",
                    label="",
                    className="three columns",
                    n_clicks=0,
                    style={
                        "paddingTop": "1%",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
                # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                #              "excel/dash-daq/dash-daq-logo-by-plotly-stripe.png",
                #          style={'position': 'relative',
                #                 'float': 'right',
                #                 'right': '10px',
                #                 'height': '75px'})
            ],
            className='row',
            style={
                'height': '75px',
                'margin': '0px -10px 10px',
                'background-color': '#EBF0F8'
            },
        ),
        html.Div(
            [
                html.H3("XYZ Controller Info", className="six columns"),
            ],
            className='row Title',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div("Attached:", className="two columns"),
                        html.Div("Disconnected",
                                 id="device-attached",
                                 className="nine columns"),
                        daq.Indicator(
                            id="connection-est",
                            value=False,
                            className="one columns",
                            style={'margin': '6px'}
                        )
                    ], className="row attachment"
                ),
                html.Hr(style={'marginBottom': '0', 'marginTop': '0'}),
                html.Div(
                    [
                        html.Div("Version:", className="two columns"),
                        html.Div("Disconnected",
                                 id="device-version",
                                 className="four columns"),
                        html.Div("Serial Number:", className="two columns"),
                        html.Div("Disconnected", id="device-serial")
                    ],
                    className="row version-serial",
                ),
            ],
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("XYZ-Setting")
                            ],
                            className='Title',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="x-set",
                                            placeholder="x-position",
                                            type="text",
                                            value="",
                                            className="three columns",
                                            style={
                                                "width": "22%",
                                                "marginLeft": "0%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Button(
                                            'Move X',
                                            id="x-move",
                                            className="one columns",
                                            n_clicks=0,
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginLeft": "1%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Actual X:",
                                                    style={
                                                        "marginLeft": "12%",
                                                        "marginTop": "5%"},
                                                    className="three columns"),
                                                html.Div(
                                                    id="x-value",
                                                    className="two columns",
                                                    style={
                                                        "marginTop": "5%",
                                                        'marginRight': '20px'}),
                                                html.Div(
                                                    "mm",
                                                    className="one columns"),
                                            ],
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="y-set",
                                            placeholder="y-position",
                                            type="text",
                                            value="",
                                            className="three columns",
                                            style={
                                                "width": "22%",
                                                "marginLeft": "0%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Button(
                                            'Move Y',
                                            id="y-move",
                                            className="one columns",
                                            n_clicks=0,
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginLeft": "1%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Actual Y:",
                                                    style={
                                                        "marginLeft": "12%",
                                                        "marginTop": "5%"},
                                                    className="three columns"),
                                                html.Div(
                                                    id="y-value",
                                                    className="two columns",
                                                    style={
                                                        "marginTop": "5%",
                                                        'marginRight': '20px'}),
                                                html.Div(
                                                    "mm",
                                                    className="one columns"),
                                            ],
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="z-set",
                                            placeholder="z-position",
                                            type="text",
                                            value="",
                                            className="three columns",
                                            style={
                                                "width": "22%",
                                                "marginLeft": "0%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Button(
                                            'Move Z',
                                            id="z-move",
                                            className="one columns",
                                            n_clicks=0,
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginLeft": "1%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Actual Z:",
                                                    style={
                                                        "marginLeft": "12%",
                                                        "marginTop": "5%"},
                                                    className="three columns"),
                                                html.Div(
                                                    id="z-value",
                                                    className="two columns",
                                                    style={
                                                        "marginTop": "5%",
                                                        'marginRight': '20px'}),
                                                html.Div(
                                                    "mm",
                                                    className="one columns"),
                                            ],
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="vel-set",
                                            placeholder="velocity",
                                            type="text",
                                            value="",
                                            className="three columns",
                                            style={
                                                "width": "22%",
                                                "marginLeft": "0%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                        html.Button(
                                            'Pattern',
                                            id="pattern",
                                            className="one columns",
                                            n_clicks=0,
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginLeft": "1%",
                                                "marginTop": "3%",
                                            },
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),

                    ],
                    className="six columns",
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Laser Settings")
                            ], className='Title'
                        ),
                        html.Div(
                            [
                                daq.BooleanSwitch(
                                    id='flipper-switch',
                                    on=False,
                                ),
                                html.Div(
                                    id='flipper-switch-output')
                            ], className="row"
                        ),
                    ], className='three columns'
                ),

            ],
        ),
        # Placeholder Divs
        html.Div(
            [
                html.Div(id="div-one"),
                html.Div(id="stop-all"),
                html.Div(id="move-x"),
                html.Div(id="move-y"),
                html.Div(id="move-z"),
                # html.Div(id="div-four"),
                # html.Div(id="com-value"),
                # html.Div(id="color-return"),
                # html.Div(id="velocity-store"),
                # dcc.Interval(id="velocity-interval", interval=360000, n_intervals=0),
            ],
            style={"visibility": "hidden"},
        ),
        # html.Div(id='div-one'),

    ], className="twelve columns"
)

app.layout = root_layout


# # Preset Settings
# @app.callback(
#     Output("div-one", "children"),
#     [Input("x-set", "n_submit"),
#      Input("y-set", "n_submit"),
#      Input("z-set", "n_submit")],
#     [State('x-set', 'value'),
#      State("y-set", "value"),
#      State("z-set", "value")]
# )
# def moving_xy(nsx, nsy, nsz, xpos, ypos, zpos):
#     xcom = "{}".format(xpos)
#     ycom = "{}".format(ypos)
#     zcom = "{}".format(zpos)
#
#     ctrl.x.position = float(xcom)
#     ctrl.y.position = float(ycom)
#     ctrl.phi.position = float(zcom)
#     return xpos, ypos, zpos


# Move Button
@app.callback(
    Output("move-x", "children"),
    [Input("x-move", "n_clicks")],
    [State("x-set", "value")]
)
def x_button(n_clicks, value):
    if n_clicks >= 1:
        ctrl.x.enable()
        x = "{}".format(value)
        ctrl.x.position = float(x)
    else:
        return


# Move Button
@app.callback(
    Output("move-y", "children"),
    [Input("y-move", "n_clicks")],
    [State("y-set", "value")]
)
def y_button(n_clicks, value):
    if n_clicks >= 1:
        ctrl.y.enable()
        y = "{}".format(value)
        ctrl.y.position = float(y)
    else:
        return


# Move Button
@app.callback(
    Output("move-z", "children"),
    [Input("z-move", "n_clicks")],
    [State("z-set", "value")]
)
def z_button(n_clicks, value):
    if n_clicks >= 1:
        ctrl.phi.enable()
        z = "{}".format(value)
        ctrl.phi.position = float(z)
    else:
        return


# ### Enable laser ###
# @app.callback(
#     Output('flipper-switch-output', 'children'),
#     [Input('flipper-switch', 'on')])
# def laser(on):
#     """Switch 'on' or 'off'"""
#     # Raw byte commands for "MGMSG_MOT_MOVE_JOG".
#     #     on = b"\x6A\x04\x00\x01\x21\x01"  # x01 up
#     #     off = b"\x6A\x04\x00\x02\x21\x01"  # x02 down
#
#     if on:
#         motor = ftd2xx.openEx(serial)
#         print(motor.getDeviceInfo())
#         motor.setBaudRate(115200)
#         motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
#         sleep(.05)
#         motor.purge()
#         sleep(.05)
#         motor.resetDevice()
#         motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
#         motor.setRts()
#
#         # Send raw bytes to USB driver.
#         motor.write(b"\x6A\x04\x00\x01\x21\x01")  # up or
#         motor.close()
#         return 'The laser is on : {}' .format(on)
#     else:
#         motor = ftd2xx.openEx(serial)
#         print(motor.getDeviceInfo())
#         motor.setBaudRate(115200)
#         motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
#         sleep(.05)
#         motor.purge()
#         sleep(.05)
#         motor.resetDevice()
#         motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
#         motor.setRts()
#
#         # Send raw bytes to USB driver.
#         motor.write(b"\x6A\x04\x00\x02\x21\x01")  # up or
#         motor.close()
#         return 'The laser is on : {}' .format(on)
#
# ### Status XYZ Positions ###
# @app.callback(Output("x-value", "children"),
#               [Input("stream", "n_intervals")],
#               [State("connection-est", "value")])
# def stream_x(_, connection):
#     if connection:
#         return ctrl.x.position
#     return str(0)
#
# @app.callback(Output("y-value", "children"),
#               [Input("stream", "n_intervals")],
#               [State("connection-est", "value")])
# def stream_y(_, connection):
#     if connection:
#         return ctrl.y.position
#     return str(0)
#
# # @app.callback(Output("z-value", "children"),
# #               [Input("stream", "n_intervals")],
# #               [State("connection-est", "value")])
# # def stream_z(_, connection):
# #     if connection:
# #         return ctrl.phi.position
# #     return str(0)
#
### XYZ Device Connection ###
@app.callback(Output("device-attached", "children"),
              [Input("connection-est", "value")])
def device_name(connection):
    if connection:
        return ctrl.name


@app.callback(Output("device-version", "children"),
              [Input("connection-est", "value")])
def device_version(connection):
    if connection:
        return ctrl.id


#
#
### Connection stream ###
@app.callback(Output("connection-est", "value"),
              [Input("upon-load", "n_intervals")])
def connection_established(_):
    if ctrl.name is not None:
        return True


@app.callback(Output("upon-load", "interval"),
              [Input("upon-load", "n_intervals"),
               Input("connection-est", "value")])
def load_once(_, connection):
    if connection is True:
        return 3.6E6
    return 1000


#
# Stop Button Terminate
@app.callback(
    Output("stop-all", "children"),
    [Input("start-stop", "n_clicks")]
)
def start_terminate(stop):
    if stop >= 1:
        ctrl.x.disable()
        ctrl.y.disable()
        ctrl.phi.disable()
        return
    else:
        response = "Terminate commands and flush serial."
        return response


if __name__ == '__main__':
    # defaultset()
    app.run_server(port=8800, debug=True)
