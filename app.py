from flask import Flask, render_template, request
import pandas as pd
#from bokeh.charts import Histogram
from bokeh.embed import components
import requests
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)


tday = '20170911'
bday = '20170611'
feature_names = ['Adjusted Open', 'Adjusted High', 'Adjusted Low', 'Adjusted Closed']

# Create the main plot
def create_figure(current_feature_name,current_stock_name,current_df):

    current_df['date'] = pd.to_datetime(current_df['date'])
    
    # Title
    pname = 'Stock '+ current_stock_name + ' at ' + current_feature_name + ' price.'
    
    # create a new plot with a datetime axis type
    p = figure(plot_width=800, plot_height=250, x_axis_type="datetime",title=pname)
    
    # Set the x axis label
    p.xaxis.axis_label = 'Date'
    
    # Set the y axis label
    p.yaxis.axis_label = current_feature_name
    
    p.line(current_df['date'], current_df[current_feature_name], color='navy', alpha=0.5)
    
    return p

# Index page
@app.route('/')
def index():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "adj_open"
    if current_feature_name == 'Adjusted Open':
        current_feature_name = "adj_open"
    if current_feature_name == 'Adjusted High':
        current_feature_name = "adj_high"
    if current_feature_name == 'Adjusted Low':
        current_feature_name = "adj_low"
    if current_feature_name == 'Adjusted Closed':
        current_feature_name = "adj_close"
    
    # Determine the Stock
    #    current_stock_name == 'MSFT'
    current_stock_name = request.args.get("current_stock" )
    if current_stock_name == None:
        current_stock_name = 'MSFT'
    #
    #    ticker = 'MSFT'
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=' \
        + bday + '&date.lt=' + tday + '&ticker=' + current_stock_name + '&api_key=N_7w_cTE9bSpuy-9U6PG'
    r = requests.get(url)
    j = r.json()
    t = j['datatable']
    df = pd.DataFrame(t['data'],columns=[ d['name'] for d in t['columns']] )

    # Create the plot
    plot = create_figure(current_feature_name,current_stock_name, df)
    
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div,
                           feature_names=feature_names,  current_feature_name=current_feature_name,
                           current_stock = current_stock_name)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=33507)
