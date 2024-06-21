"""
Module Name:    Viz Tools
Author:         Carlos Alberto Toruño Paniagua
Date:           May 20th, 2024
Description:    This module contains all the functions and classes to be used by the EU Copilot 
                Dashboard for visualizing GPP data.
This version:   May 24th, 2024
"""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


def genBars(data, cpal, level):

    if level  == "EU":
        fig = px.bar(
            data, 
            x = "value_realign", 
            y = "title",
            color = "value_realign", 
            orientation  = "h",
            range_color  = [0,100],
            custom_data  = ["title", "value_realign", "direction"],
            color_continuous_scale = cpal,
            color_continuous_midpoint = 50
        )
        fig.update_traces(
            hovertemplate = "<b>%{customdata[0]}</b><br>Value: %{customdata[1]:.1f}%<br><i>Direction: %{customdata[2]}</i>",
            marker = dict(showscale = False)
        )
        fig.update(
            layout_coloraxis_showscale=False
        )
        fig.update_layout(
            xaxis_title = "Percentage (%)",
            yaxis_title = None,
            showlegend  = False,
            margin = {"r":0,"t":0,"l":0,"b":0},
            xaxis  = dict(
                range = [0, 100],
                dtick = 20
            ),
            yaxis = dict(
                tickmode = "linear"
            ),
            hoverlabel = dict(
                bgcolor     = "white",
                font_size   = 15,
                font_family = "Lato"
            )
        )

    if level == "indicator":
        fig = px.bar(
            data, 
            x = "value2plot", 
            y = "country_name_ltn",
            color = "value2plot", 
            orientation  = "h",
            range_color  = [0,100],
            custom_data  = ["country_name_ltn", "value2plot"],
            color_continuous_scale = cpal,
            color_continuous_midpoint = 50
        )
        fig.update_traces(
            hovertemplate="%{customdata[0]}<br><i>Value: %{customdata[1]:.1f}%</i>"
        )
        fig.update_layout(
            xaxis_title = "Percentage (%)",
            yaxis_title = None,
            showlegend  = False,
            margin = {"r":0,"t":0,"l":0,"b":0},
            xaxis  = dict(
                range = [0, 100],
                dtick = 20
            ),
            yaxis = dict(
                tickmode = "linear"
            ),
            coloraxis_colorbar = dict(
                title   = "Percentage(%)",
                y       = 1.2,
                yanchor = "top", 
                orientation = "h",
                tickvals = [0, 20, 40, 60, 80, 100],
                ticktext = ["0%", "20%", "40%", "60%", "80%", "100%"]
            ),
            hoverlabel = dict(
                bgcolor     = "white",
                font_size   = 15,
                font_family = "Lato"
            )
        )
    
    return fig

def genMetrics(n, df, d = ""):
    subsection = df.iloc[n]["subsection"]
    avg_value  = round(df.iloc[n]["average_value"], 1)
    card = st.metric(f":{d}[{subsection}]", f"Avg: {avg_value}")
    return card

def wrap_text(text):
    if len(text) <= 30:
        return text
    
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= 40:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return '<br>'.join(lines)

def genScatter(data, xtitle, ytitle, color_map):
    fig = px.scatter(
            data, 
            x = "xaxis", 
            y = "yaxis", 
            color = "xaxis",
            trendline   = "ols",
            custom_data = ["country_name_ltn", "nuts_id", "nameSHORT", "xaxis", "yaxis"],
            color_continuous_scale    = color_map,
             trendline_color_override = "red"
        )
    fig.update(
        layout_coloraxis_showscale = False
    )
    fig.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b><br>%{customdata[2]}<br>" + f"<i>{xtitle}: " + "%{customdata[3]:.1f}%</i><br>" + f"<i>{ytitle}: " + "%{customdata[4]:.1f}%</i><br>"
    )
    fig.update_layout(
        xaxis_title = xtitle,
        yaxis_title = ytitle,
        showlegend  = False,
        margin = {"r":0,"t":25,"l":0,"b":0},
        xaxis  = dict(
            range     = [0, 100],
            dtick     = 20,
            showline  = True,
            mirror    = True,
            linewidth = 1,
            linecolor = "black"
        ),
        yaxis  = dict(
            range     = [0, 100],
            dtick     = 20,
            showgrid  = False,
            showline  = True,
            mirror    = True,
            linewidth = 1,
            linecolor = "black",
            zeroline  = False
        ),
        hoverlabel = dict(
            bgcolor     = "white",
            font_size   = 15,
            font_family = "Lato"
        )
    )
    return fig

def genBees(country_data, country_select):

    ntopics = len(
        country_data
        .loc[country_data["level"] == "national"]
        .drop_duplicates(subset = "subsection")
        .subsection.to_list()
    )

    country_data["subsection"] = country_data["subsection"].apply(wrap_text)

    fig = px.strip(
        country_data, 
        y = "subsection", 
        x = "value_realign", 
        stripmode   = "group",
        color       = "country_name_ltn", 
        custom_data = ["title", "value_realign", "country_name_ltn"]
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[2]}</b><br>%{customdata[0]}<br><i>Value: %{customdata[1]:.1f}%</i>",
    )
    for trace in fig.data:
        trace.update(opacity = 0.05)
    fig.for_each_trace(
        lambda trace: trace.update(opacity=1.0) if trace.name in country_select else None
    )
    fig.update_layout(
        height = 275 +(ntopics*40),
        xaxis_title = None,
        yaxis_title = None,
        yaxis = dict(
            tickfont = dict(size = 14)
        ),
        template    = "plotly_white",
        showlegend  = False,
        hoverlabel = dict(
            bgcolor     = "white",
            font_size   = 15,
            font_family = "Lato"
        )
    )
    return fig

def genDotties(data, topic, groupings, stat):
    if stat == "Data Points":
        xaxis = "value2plot"
    if stat == "Deviations from National Average":
        xaxis = "dev"
    
    grouping_pattern = "|".join(groupings)

    subset4charts = (
        data.copy()
        .loc[(data["topic"] == topic) & (data["region"].str.contains(grouping_pattern))]
    )
    fig = px.scatter(
        subset4charts,
        x = xaxis,
        y = "title",
        title = topic,
        color = "region",
        color_discrete_sequence=px.colors.qualitative.G10,
        facet_col="grouping",
        facet_col_spacing = 0.04,
        category_orders={"grouping": groupings}
    )
    fig.update_layout(
        height = 400,
        xaxis_title = None,
        yaxis_title = None,
        template    = "plotly_white",
        showlegend  = False,
    )
    return fig

def genMap(data4map, eu_nuts, color_palette):
    fig = px.choropleth_mapbox(
        data4map,
        geojson      = eu_nuts,
        locations    = "nuts_id",
        featureidkey = "properties.polID",
        mapbox_style = "carto-positron",
        center       = {"lat": 52.250, "lon": 13.025},
        custom_data  = ["country_name_ltn", "nameSHORT", "value2plot"],
        zoom         = 3,
        color        = "value2plot",
        range_color  = [0,100],
        color_continuous_scale    = color_palette,
        color_continuous_midpoint = 50
    )
    fig.update_traces(
        hovertemplate="%{customdata[1]}<br><i>%{customdata[0]}</i><br>Value: %{customdata[2]:.1f}%",
    )
    fig.update_layout(
        height = 800,
        coloraxis_colorbar = dict(
            title   = "Percentage(%)",
            x       = 0,
            xanchor ="left",
            y       = 1.1,
            yanchor = "top", 
            orientation = "h", 
            tickvals = [0, 20, 40, 60, 80, 100],
            ticktext = ["0%", "20%", "40%", "60%", "80%", "100%"]
        ),
        hoverlabel = dict(
            bgcolor     = "white",
            font_size   = 15,
            font_family = "Lato"
        )
    )
    return fig


def genDumbbell(subset_df, subsection):

    fig = go.Figure()

    for index, row in subset_df.iterrows():

        fig.add_trace(go.Scatter(
            x = [row['eu_value'], row['country_value']],
            y = [row['title'], row['title']],
            mode = 'lines+markers+text',
            marker = dict(size = 13, color = ['blue', 'red']),
            line = dict(color = 'gray'),
            text = [None, f"{row['difference']:+.2f}"],
            textposition = 'middle right' if row['difference'] > 0 else 'middle left',
            textfont = dict(color = 'green' if row['difference'] > 0 else 'red'),
            hoverinfo='text',
            hovertext = f"<br><i>{wrap_text(row['subtitle'])}</i></b><br><b>Reported {wrap_text(row['country_name_ltn'])} Value:</b> {row['country_value']:.1f}<br><b>Reported EU Value:</b> {row['eu_value']:.1f}",
            hoverlabel=dict(font_size=13, align='left')
        ))

    fig.update_layout(
        title = subsection,
        height = 400,
        width = 800,
        xaxis = dict(range = [0,100]),
        yaxis = dict(showgrid = False),
        xaxis_title = None,
        yaxis_title = None,
        template = "plotly_white",
        showlegend = False,
        margin=dict(l=50, r=50, t=50, b=50)

    )

    return fig
    

def genRankingsViz(subset_df, subsection, chosen_country):

    color_scale = px.colors.qualitative.G10
    subset_df['subtitle'] = subset_df['subtitle'].apply(wrap_text)


    fig = px.scatter(
        subset_df,
        x = 'ranking',
        y = 'title', # wrap 
        title = f'{subsection}',
        color = 'country_name_ltn',
        color_discrete_sequence=color_scale,
        custom_data=['country_name_ltn', 'value2plot', 'subtitle', 'ranking'],
        range_color=[1,27]
    )

    # opacity of chosen country bolded, every thing else faded
    for trace_index, country in enumerate(subset_df['country_name_ltn']):
        opacity = 1 if country == chosen_country else 0.1
        fig.update_traces(selector=dict(name=country), opacity=opacity)

    fig.update_traces(
    hovertemplate="<br>".join([
        "<b><span style='font-size: 14px;'>%{customdata[0]}</span></b>",  
        "<i><b>Reported Value: %{customdata[1]:.1f}</i>",
        "<i>Context: %{customdata[2]}</i>",
        "Ranking: %{customdata[3]}"
    ])
    )

    fig.update_layout(
        height=450,
        width=860,
        xaxis_title='Ranking in the EU',
        yaxis_title=None,
        template="plotly_white",
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),  
        yaxis=dict(showgrid = False),  
        xaxis=dict(showgrid = False)   
    )

    fig.update_traces(marker=dict(size=11))

    return fig


def QRQ_country_scatter(df, country, chapter):
    # df should be subset by country, level = regional and contain only QRQ values
    df['section'] = df['section'].apply(wrap_text)
    national = df.loc[(df['country_name_ltn'] == country) & (df['chapter'] == chapter) &
                          (df['level'] == 'national')]
    regional_data = df.loc[(df['country_name_ltn'] == country)&(df['level'] == 'regional') & (df['chapter'] == chapter)]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = national['value2plot'],
            y = national['section'],
            mode = 'markers+text',
            marker = dict(size = 12, color = 'blue', opacity = 0.8),
            text = national['value2plot'].apply(lambda x: f"{x:.2f}"),
            textposition = "top center",
            customdata=national[['country_name_ltn', 'value2plot']],
            hovertemplate="<b>%{customdata[0]}</b><br>Mean QRQ Score: %{customdata[1]:.2f}%<br>",
            name='National'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=regional_data['value2plot'],
            y=regional_data['section'],
            mode='markers+text',
            marker = dict(size = 8, color = 'blue', opacity = 0.2),
            customdata=regional_data[['nameSHORT', 'value2plot']],
            hovertemplate="Region: %{customdata[0]}<br>Mean QRQ Score: %{customdata[1]:.2f}%<extra></extra>",
            showlegend=False,
            name = 'Regional'
        )
    )

    fig.update_layout(
    yaxis_title = 'Indicator',
    xaxis_title = 'QRQ Scores',
    showlegend = False
    )

    fig.update_layout(
        dragmode='zoom',  # Enable drag to zoom
        xaxis=dict(
            fixedrange=False,  # Allow zooming only on x-axis
        ),
        yaxis=dict(
            fixedrange=True,  # Disable zooming on y-axis
        ),
        autosize=True,
        margin=dict(
            autoexpand=True
        ),
        template='plotly_white'  # Optional: set plot template
    )

    return fig



def gen_compare_scatter(subset, section, gpp_indicator):
    subset["subtitle"] = subset["subtitle"].apply(wrap_text)
    qrq_data = subset[subset['title'] == section]
    gpp_data = subset[subset['title'] == gpp_indicator]

     # Ensure qrq_data and gpp_data are not empty before merging
    if qrq_data.empty or gpp_data.empty:
        return go.Figure().update_layout(
            title=f"No data available for {section} (QRQ) and {gpp_indicator} (GPP)",
            xaxis_title=f"{section} (QRQ Score)",
            yaxis_title=f"{gpp_indicator} (GPP value)"
        )

    merged = pd.merge(qrq_data, gpp_data, on='nuts_id', suffixes=('_qrq', '_gpp'))

    # Ensure merged data is not empty before proceeding
    if merged.empty:
        return go.Figure().update_layout(
            title=f"No data available for {section} (QRQ) and {gpp_indicator} (GPP)",
            xaxis_title=f"{section} (QRQ Score)",
            yaxis_title=f"{gpp_indicator} (GPP value)"
        )
    
    # regress
    X = merged['value2plot_qrq'].values.reshape(-1, 1)
    y = merged['value2plot_gpp'].values

    # fit model
    reg = LinearRegression().fit(X, y)
    trendline = reg.predict(X)

    # R-squared value
    r_squared = reg.score(X, y)

    # color map
    unique_countries = merged['country_name_ltn_qrq'].unique()
    num_colors = len(unique_countries)
    colors = px.colors.qualitative.Plotly

    # If there are more unique countries than colors in the palette, generate more colors
    if num_colors > len(colors):
        from itertools import cycle
        extended_colors = cycle(px.colors.qualitative.Vivid)
        colors = [next(extended_colors) for _ in range(num_colors)]

    color_map = {country: colors[i % len(colors)] for i, country in enumerate(unique_countries)}

    fig = px.scatter(
        merged,
        x = 'value2plot_qrq',
        y = 'value2plot_gpp',
        color = 'country_name_ltn_qrq',
        color_discrete_map=color_map,
        labels = {
            'value2plot_qrq': section + '(QRQ Score)',
            'value2plot_gpp': gpp_indicator + '(GPP value - %)',
            'country_name_ltn': 'nameShort'
        },
        custom_data=['nameSHORT_qrq','country_name_ltn_qrq', 'value2plot_qrq', 'value2plot_gpp', 'subtitle_gpp'],
        title = f'Scatter Plot of {section} (QRQ) vs {gpp_indicator} (GPP)'
    )

    fig.update_layout(
        showlegend = False,
        height = 450,
        width = 650,
        yaxis = dict(range=[0,100]),
        xaxis = dict(range=[0.2,1])
    )

    fig.update_traces(hovertemplate="<br>".join([
        "<b><span style='font-size: 14px;'>%{customdata[0]}, %{customdata[1]}</span></b>",  
        "<i><b>QRQ Score: %{customdata[2]:.2f}</i>",
        "<i><b>GPP Value: %{customdata[3]:.1f}%</i>",
        "<i>GPP Context: %{customdata[4]}</i>"
    ]))
    

    fig.update_traces(marker=dict(size=7))

        # Add trendline
    fig.add_trace(
        go.Scatter(
            x=merged['value2plot_qrq'],
            y=trendline,
            mode='lines',
            line=dict(color='red'),
            name='Trendline'
        )
    )

    # Add R-squared annotation
    fig.add_annotation(
        x=max(merged['value2plot_qrq']),
        y=min(merged['value2plot_gpp']),
        text=f'R² = {r_squared:.2f}',
        showarrow=False,
        font=dict(size=12, color='red')
    )

    return fig


def gen_qrq_rankins(df, chosen_country):
    color_scale = px.colors.qualitative.G10
    df['section'] = df['section'].apply(wrap_text) 
    df['subtitle'] = df['subtitle'].apply(wrap_text)

    chapter = df['chapter'].iloc[1]

    fig = px.scatter(
        df,
        x='ranking',
        y='section',  
        title=chapter,
        color='country_name_ltn',
        color_discrete_sequence=color_scale,
        custom_data=['country_name_ltn', 'value2plot', 'subtitle', 'ranking'],
        range_color=[1, 27]
    )

        # opacity of chosen country bolded, every thing else faded
    for trace_index, country in enumerate(df['country_name_ltn']):
        opacity = 1 if country == chosen_country else 0.1
        fig.update_traces(selector=dict(name=country), opacity=opacity)

    fig.update_traces(
    hovertemplate="<br>".join([
        "<b><span style='font-size: 14px;'>%{customdata[0]}</span></b>",  
        "<i><b>QRQ Score: %{customdata[1]:.3f}</i>",
        "<i>Context: %{customdata[2]}</i>",
        "Ranking: %{customdata[3]}"
    ])
    )

    fig.update_layout(
        height=450,
        width=860,
        xaxis_title='Ranking in the EU',
        yaxis_title=None,
        template="plotly_white",
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),  
        yaxis=dict(showgrid = False),  
        xaxis=dict(showgrid = False)   
    )

    fig.update_traces(marker=dict(size=11))

    return fig



def genQRQMap(data4map, eu_nuts, color_palette):
    fig = px.choropleth_mapbox(
        data4map,
        geojson      = eu_nuts,
        locations    = "nuts_id",
        featureidkey = "properties.polID",
        mapbox_style = "carto-positron",
        center       = {"lat": 52.250, "lon": 13.025},
        custom_data  = ["country_name_ltn", "nameSHORT", "value2plot"],
        zoom         = 3,
        color        = "value2plot",
        range_color  = [0,1],
        color_continuous_scale    = color_palette,
        color_continuous_midpoint = 0.5
    )
    fig.update_traces(
        hovertemplate="%{customdata[1]}<br><i>%{customdata[0]}</i><br>Value: %{customdata[2]:.3f}",
    )
    fig.update_layout(
        height = 800,
        coloraxis_colorbar = dict(
            title   = "Score",
            x       = 0,
            xanchor ="left",
            y       = 1.1,
            yanchor = "top", 
            orientation = "h", 
            tickvals = [0, .2, .40, .60, .80, 1],
            ticktext = ["0", "0.2", "0.4", "0.6", "0.8", "1"]
        ),
        hoverlabel = dict(
            bgcolor     = "white",
            font_size   = 15,
            font_family = "Lato"
        )
    )
    return fig


def genQRQBars(data, cpal, level):

    if level  == "EU":
        fig = px.bar(
            data, 
            x = "value_realign", 
            y = "title",
            color = "value_realign", 
            orientation  = "h",
            range_color  = [0,1],
            custom_data  = ["title", "value_realign", "direction"],
            color_continuous_scale = cpal,
            color_continuous_midpoint = 0.5
        )
        fig.update_traces(
            hovertemplate = "<b>%{customdata[0]}</b><br>Value: %{customdata[1]:.1f}%<br><i>Direction: %{customdata[2]}</i>",
            marker = dict(showscale = False)
        )
        fig.update(
            layout_coloraxis_showscale=False
        )
        fig.update_layout(
            xaxis_title = "QRQ Score",
            yaxis_title = None,
            showlegend  = False,
            margin = {"r":0,"t":0,"l":0,"b":0},
            xaxis  = dict(
                range = [0, 1],
                dtick = 20
            ),
            yaxis = dict(
                tickmode = "linear"
            ),
            hoverlabel = dict(
                bgcolor     = "white",
                font_size   = 15,
                font_family = "Lato"
            )
        )

    if level == "indicator":
        fig = px.bar(
            data, 
            x = "value2plot", 
            y = "country_name_ltn",
            color = "value2plot", 
            orientation  = "h",
            range_color  = [0,1],
            custom_data  = ["country_name_ltn", "value2plot"],
            color_continuous_scale = cpal,
            color_continuous_midpoint = .5
        )
        fig.update_traces(
            hovertemplate="%{customdata[0]}<br><i>Score: %{customdata[1]:.3f}</i>"
        )
        fig.update_layout(
            xaxis_title = "QRQ Score",
            yaxis_title = None,
            showlegend  = False,
            margin = {"r":0,"t":0,"l":0,"b":0},
            xaxis  = dict(
                range = [0, 1],
                dtick = 20
            ),
            yaxis = dict(
                tickmode = "linear"
            ),
            coloraxis_colorbar = dict(
                title   = "QRQ Score",
                y       = 1.2,
                yanchor = "top", 
                orientation = "h",
                tickvals = [0, .2,.4,.6,.8,1],
                ticktext = ["0", "0.2", "0.4", "0.6", "0.8", "1"]
            ),
            hoverlabel = dict(
                bgcolor     = "white",
                font_size   = 15,
                font_family = "Lato"
            )
        )
    
    return fig


    

